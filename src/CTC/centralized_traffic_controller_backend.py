'''
Author: Aaron Kuchta
Date: 4-16-2025
'''


import sys
import os
import time
import queue 
import pandas as pd
import openpyxl 
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

#from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
#from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
import globals.track_data_class as global_track_data
import globals.global_clock  as global_clock
import globals.signals as signals


class CtcBackEnd(QObject):
    def __init__(self): 
        super().__init__()
        #Controls active track data
        self.green_line = Track("Green")
        #self.red_line = Track("Red") #No red line implementation yet
        self.active_line = self.green_line

        self.train_queue = queue.Queue()

        self.wall_clock = global_clock.clock

        #Read in signal from Track Model
        signals.communication.track_tickets.connect(self.update_tickets)  #int
        signals.communication.wayside_block_occupancies.connect(self.update_occupancy) #List
        signals.communication.wayside_plc_outputs.connect(self.update_from_plc)
        
        
        self.suggested_speed = {} #key is block data is sent to
        self.suggested_authority = {} #Key is block data is being sent to

        self.total_tickets = 0
        self.throughput = 0
        self.elapsed_mins = 0
        self.last_minute = self.wall_clock.minute

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.backend_update)
        self.timer.start(self.wall_clock.ctc_dt)  # 10 Hz update

        

    def backend_update(self):
        if self.wall_clock.minute != self.last_minute:
            self.elapsed_mins += 1
            self.last_minute = self.wall_clock.minute
        self.dispatch_queue_handler() #Dispatch queue handler  
        self.active_train_handler()
        

    def get_map_data(self):
        return self.active_line.blocks, self.active_line.station_names, self.active_line.switch_data, self.active_line.switch_states, self.active_line.lights, self.active_line.crossings

    def process_route_data(self, file_data):
        if(file_data is not None):
            self.read_route_file(file_data)

    def read_route_file(self, file_data):
        for _, row in file_data.iterrows():
            #Get the route name
            route_name = row.iloc[0]  #Think about storing for refrence?
            #print("Route Name: ", route_name)
            
            #Get all the station names
            stations = row[1:].dropna().tolist()

            # Check if the route name already exists in the routes dictionary
            if route_name not in self.active_line.routes:
                self.active_line.routes[route_name] = []  # Initialize an empty list for new routes
            self.active_line.routes[route_name].extend(stations)

            #print(f"{route_name}: {', '.join(stations[0])}")


    def update_manual_suggested(self):
        if self.ctc_ui.sub_enter_speed_override.value() > 0:
            self.update_manual_speed()

        if self.ctc_ui.sub_enter_authority_override.value() > 0:
            self.update_manual_authority()

    def update_override_speed(self):
        #updates override speed | input from user
        override_speed = self.ctc_ui.sub_enter_speed_override.text()
        self.test_bench.print_suggested_speed(override_speed)
    
    def update_override_authority(self):
        #updates override authority | input from user
        override_authority = self.ctc_ui.sub_enter_authority_override.text()
        self.test_bench.print_suggested_authority(override_authority)

    @pyqtSlot(int)
    def update_tickets(self, num_tickets):
        #Takes tickets sold from track model and updates throughput
        self.total_tickets += num_tickets
        self.throughput = self.total_tickets / (self.elapsed_mins/60) #Tickets per hour

    @pyqtSlot(dict)
    def update_occupancy(self, occupancies):
        #Updates occupancy list | called by wayside controller
        for i, block in enumerate(self.active_line.blocks):
             if block.id in occupancies:
                 self.active_line.blocks[i].occupancy = occupancies[block.id]
            

    @pyqtSlot(list,list,list,list)
    def update_from_plc(self, sorted_blocks, switches, lights, crossings):
        switch_index = 0
        light_index = 0
        crossing_index = 0

        for block_index, block in enumerate(sorted_blocks): # each WAYSIDE sends its portion of the track sorted by territory

            if block.switch: # if the block has a switch
                self.active_line.blocks[block_index].switch_state = switches[switch_index] # plc outputs have there own index since the first switch isnt at the first block etc.
                switch_index += 1

            if block.light:
                self.active_line.blocks[block_index].light_state = lights[light_index]
                light_index += 1
            
            if block.crossing:
                self.active_line.blocks[block_index].crossing_state = crossings[crossing_index]
                crossing_index += 1


    def get_expected_next_block(self, train): #may need to be updated to include switch states
            #Check each block in line
            for block in self.active_line.blocks:
                #ensure current train location
                if block.occupancy and block.id == train.current_block:
                    
                    if train.current_block == self.active_line.EXIT_BLOCK:
                        return -1 #Train reached ending block

                    #Get direction of train
                    section_key = block.id[0]  # Get section letter
                    section_dir = self.active_line.sections[section_key].increasing

                    #update train direction if not bidirectional
                    if section_dir != 2:  
                        train.direction = section_dir

                    jump_key = (int(block.id[1:]), train.direction)
                    #Check if train is at jump block
                    if jump_key in self.active_line.JUMP_BLOCKS:
                        next_block, new_dir = self.active_line.JUMP_BLOCKS[jump_key]
                        train.direction = new_dir
                        return self.active_line.blocks[next_block - 1].id
                    
                    #if moving in decreasing direction
                    if train.direction == 0:
                        return self.active_line.blocks[int(block.id[1:]) - 2].id
                    #if moving in increasing direction
                    elif train.direction == 1:
                        return self.active_line.blocks[int(block.id[1:])].id

            #if no block occupancy, set to entrance block - not needed?
            #return self.active_line.blocks[self.active_line.ENTRANCE_BLOCK - 1].id

    def update_train_location(self):
        for train in self.active_line.current_trains:
            #Check if train moved to next block
            for block in self.active_line.blocks:
                if block.id == train.next_block and block.occupancy:
                    train.current_block = train.next_block
                    train.next_block = self.get_expected_next_block(train)
                    #print("[CTC DEBUG] Train ID: ", train.train_id, "Current Block: ", train.current_block, "Next Block: ", train.next_block)
                    if train.next_block == -1:
                        print("Train ID: ", train.train_id, "Exiting the line")
                        self.active_line.current_trains.remove(train) #Remove train from active trains
                    break


    def active_train_handler(self):
        for train in self.active_line.current_trains:
            # print("Train ID: ", train.train_id, "Current Block: ", train.current_block)
            if int(train.current_block[1:]) == self.active_line.ENTRANCE_BLOCK and not train.received_first_auth:
                suggested_speed, suggested_authority = self.get_suggestion_values(train)
                self.send_suggestions(suggested_speed, suggested_authority) #Send suggestions to wayside
                train.received_first_auth = True # Only send once when entering the line
            if train.get_next_stop(): # make sure there are stops left
                # Did you make it to the stop
                if train.current_block == self.active_line.blocks[train.get_next_stop()-1].id:
                    train.route_index += 1 # You made it to the stop
                    # Now that the train has reached its first stop, enable middle-of-block adjustment.
                    train.middle_adjust = True
                    
                    # if we made it the last stop, the get_suggestion_values will be empty dicts
                    suggested_speed, suggested_authority = self.get_suggestion_values(train)
                    self.send_suggestions(suggested_speed, suggested_authority) #Send suggestions to wayside
                    
            self.update_train_location()
            
            #print("Current Block", train.current_block, "Route: ", train.get_next_stop())


    def first_blocks_free(self):
        #Checks if first blocks are free | called by dispatch queue handler
        block_1 = self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].occupancy or self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].maintenance
        #print("Block ", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].id, "Occupancy is", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].occupancy, " and has maintenance ", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].maintenance)
        if not block_1: # Altered from 3 blocks
            return True
        else:
            return False

    def dispatch_handler(self, destination, destination_type, new_train=True):
        #Train dispatch handler | called by front end
        full_route = []
        if destination_type == 'station':
            #Dispatch to station
            destination_set = int(self.active_line.STATIONS_BLOCKS[destination])
            full_route.append(destination_set) #Maybe Temporary
            #full_route = self.calculate_authority(self.active_line.ENTRANCE_BLOCK, destination_set) # UNUSED
            #print("Trying to dispatch to: ", destination, " Block: ", destination_set, "With Authority: ", full_route)

        elif destination_type == 'block':
            #Dispatch to block
            destination_set = int(destination)
            full_route.append(destination_set) #Maybe Temporary
            #full_route = self.calculate_authority(self.active_line.ENTRANCE_BLOCK, destination_set) #Calculate authority to block
            #print("Trying to dispatch to block", destination, "With Authority: ", full_route)
            
        elif destination_type == 'route':
            #Dispatch on a route
            last_block = self.active_line.ENTRANCE_BLOCK #Starting track block
            
            route_stations = (self.active_line.routes[destination]) #Get first block of route
            #print("Train destination route: ", route_stations)
            for stations in self.active_line.routes[destination]:
                next_block = (self.active_line.STATIONS_BLOCKS[stations])
                #print("Station ", stations, "Block ", next_block)
                #auth = self.calculate_authority(last_block, next_block)
                full_route.append(next_block)
                #print("Full route: ", full_route)
                #print("Auth to block", next_block, "from block", last_block, "is ", auth)
                last_block = next_block #Update last block to current block
                
            #print("Full route: ", full_route)
        if new_train:
            new_train = DummyTrain(self.active_line.train_ID_count, full_route, "manual", "y151")
            self.active_line.train_ID_count += 1
            self.train_queue.put(new_train) 
        else:
            self.active_line.current_trains[0].set_route(full_route)
            speed, auth = self.get_suggestion_values(self.active_line.current_trains[0])
            self.send_suggestions(speed, auth)
        #print("Train Entered into Queue")

    def dispatch_queue_handler(self):
        # Handles train queue | called by update function
        if not self.train_queue.empty() and self.first_blocks_free():
            #get train object from queue
            dispatching_train = self.train_queue.get()
            self.active_line.add_train_object(dispatching_train) #Add train to active line trains
            self.active_line.active_trains_count += 1 #Increment train count
            self.send_dispatch_train() 
 
    def send_dispatch_train(self):
        signals.communication.ctc_dispatch.emit() # Just signal, no param
        print("Train Dispatched from CTC")

    def send_block_maintenance(self, block_id, maintenance_val):
        signals.communication.ctc_block_maintenance.emit(self.active_line.blocks[block_id].id, maintenance_val) #int, bool 
        #print("Set Block ", block_id, " Maintenance value to ", maintenance_val)
        #print("Stored Block value: ", self.active_line.blocks[block_id].id, " ", self.active_line.blocks[block_id].maintenance)

    def get_suggestion_values(self, train, speed=70):
        if train.get_next_stop():
            new_speed = speed
            auth = self.calculate_authority(int(train.current_block[1:]), train.get_next_stop(), adjust=train.middle_adjust)
            # if going to yard go a little extra
            if self.active_line.blocks[train.get_next_stop()-1].id[0]=='y':
                auth += 300
            print(f"auth: {auth}")
            suggested_speed = {train.current_block : new_speed}
            suggested_authority = {train.current_block : auth}
            return suggested_speed, suggested_authority
        return {}, {}

    def send_suggestions(self, suggested_speeds, suggested_authorities):
        signals.communication.ctc_suggested.emit(suggested_speeds, suggested_authorities) #Dict, Dict

    def send_exit_blocks(self, exit_blocks):
        signals.communication.ctc_exit_blocks.emit() #List, Currently Unused

    def send_switch_states(self, block_id, switch_state): #KNOWN ERROR - SENDS SWITCH VAL WHEN EXITING MAINTENANCE
        switch_id = self.active_line.blocks[block_id].id
        signals.communication.ctc_switch_maintenance.emit(switch_id, switch_state) #String, bool
        #print("Switch on Block ", switch_id, " set to ", switch_state)

    
    def calculate_authority(self, start_id, end_id, direction=1, adjust=False):
        '''
        Parameters:
            start_id: The block ID to start from (1-150)
            end_id: The block ID to end on (1-150)
            direction: Starting movment direction, 0 for decreasing, 1 for increasing
            adjust: Boolean flag. If True, subtract half of the start block length and half of the
                    destination block length to account for the train being in the middle of a block.

        Returns: 
            Authority needed to reach end from start
    
        TODO:
            - Adapt for red line
            - Adapt for yard entrance/exit blocks
        '''

        print(start_id)
        print(end_id)
        start_id -= 1 #Convert to 0-indexed
        end_id -= 1 #Convert to 0-indexed
        current_id = start_id
        
        if start_id == end_id:
            return 0
        if not (0 <= start_id < len(self.active_line.blocks)) or not (0 <= end_id < len(self.active_line.blocks)):
            print("-----ERROR! Invalid block ID-----")
            return -1
        
        authority = 0

        #Potentially Obsolete Code
        #last_dir = direction #Initial direction
        #section_dir = self.active_line.sections[self.active_line.blocks[start_id].id[0]].increasing #0 for decreasing, 1 for increasing, 2 for bidirectional
        #print("Block: ", self.active_line.blocks[start_id].id, "Direction: ", section_dir)

        while current_id != end_id:
            #Added bounds check
            if not (0 <= current_id < len(self.active_line.blocks)):
                print("-----ERROR! Current ID out of range:", current_id, "-----")
                return -1
            
            current_block = self.active_line.blocks[current_id]
            section_key = current_block.id[0]  #Gets section letter
            section_dir = self.active_line.sections[section_key].increasing

            if section_dir != 2:
                direction = section_dir

            jump_key = (current_id+1, direction)
            #print("Current Block: ", current_block.id, "Direction: ", direction, "Jump Key: ", jump_key)

            if jump_key in self.active_line.JUMP_BLOCKS:
                #print("JUMP BLOCK DETECTED - ", current_block.id, "Direction: ", direction, "Jump Key: ", jump_key)
                next_id, new_dir = self.active_line.JUMP_BLOCKS[jump_key]
                next_id -= 1 #Convert to 0-indexed
                direction = new_dir
            else:
                if direction == 0:
                    next_id = current_id - 1
                elif direction == 1:
                    next_id = current_id + 1

            if not (0 <= next_id < len(self.active_line.blocks)):
                print("-----ERROR! Next ID out of range:", next_id, "-----")
                return -1

            if next_id != end_id:
                authority += current_block.length #accumulate authority
            #print("Current Block: ", self.active_line.blocks[current_id].id, "Next Block: ", self.active_line.blocks[next_id].id, "Direction: ", direction, "Total Authority: ", authority)

            current_id = next_id #Update current block


        current_block = self.active_line.blocks[current_id] 
        authority += (current_block.length) #Add half block authority to stop in the middle of block
        
        # if adjustment is required, subtract half the starting block and add half the destination block lengths.
        if adjust:
            authority = authority - (self.active_line.blocks[start_id].length / 2) + (self.active_line.blocks[end_id].length / 2)
        # Else just add half the destination blocks length
        else:
            authority = authority + (self.active_line.blocks[end_id].length / 2)

        #print("-----END REACHED-----")
        #print("Current Block: ", current_block.id, "Total Authority: ", authority)
        return round(authority,2)


class DummyTrain:
    def __init__(self, train_id, route, mode, start_block):
        super().__init__()
        self.train_id = train_id
        self.route = route
        self.route_index = 0
        self.mode = mode
        self.current_block = start_block 
        self.next_block = "K63" #First block out of yard on green line
        self.direction = 1 #1 for increasing, 0 for decreasing
        self.speed = 0
        self.authority = 0

        # Debugging
        self.received_first_auth = False
        
        # Flag to indicate if we should adjust for the train being in the middle of a block.
        self.middle_adjust = False

    def set_current_block(self, block_id):
        self.current_block = block_id

    def set_authority(self, authority):
        self.authority = authority
    
    def set_mode(self, mode):
        self.mode = mode

    def set_route(self, route):
        self.route_index = 0
        self.route = route

    def get_next_stop(self):
        # encapsulates this functionality
        # returns none if there are no stops left
        if self.route_index < len(self.route):
            return self.route[self.route_index]
        else:
            return None


    
class TrackBlocks:
    def __init__(self, block):
        self.id = block.id
        self.length = block.length 
        self.speed_limit = block.speed_limit
        self.grade = block.grade
        self.underground = block.underground
        self.has_station = block.station
        self.has_switch = block.switch
        self.has_light = block.light
        self.has_crossing = block.crossing
        self.has_beacon = block.beacon
        self.switch_exit = block.switch_exit

        self.occupancy = False
        self.maintenance = False
        self.switch_state = 0 #0 for first option, 1 for second option
        self.light_state = 0 #0 for red, 1 for green
        self.crossing_state = 0
        self.suggested_speed = 0
        self.suggested_authority = 0
        self.updated = True

class Track: 
    def __init__(self, name):
        self.JUMP_BLOCKS = {}  

        self.track_data = global_track_data.lines[name]
        self.name = name
        self.current_trains = []
        self.active_trains_count = 0
        self.train_ID_count = 1
        self.blocks = []
        self.sections = self.track_data.sections
        self.switch_data = self.track_data.switches
        self.station_names = self.track_data.stations
        self.switch_states = [0,0,0,0,0,0] 
        self.lights = [0,0,0,0,0,0]
        self.crossings = [0,0] 
        self.routes = {}

        if name == "Green":
            self.ENTRANCE_BLOCK = 151  #Entrance blocks for green line
            self.EXIT_BLOCK = "y152" #Exit block for green line
            self.JUMP_BLOCKS = { 
            (100, 1): (85, 0),   # Q100 -> N85, decrease
            (77, 0): (101, 1),   # N77 -> R101, increase
            (150, 1): (28, 0),   # Z150 -> F28, decrease
            (1, 0): (13, 1),    #A1 -> D13, increase
            (151, 1): (63, 1), #Yard -> K63, increase
            (57, 1): (152, 1)} #I57 -> Yard, increase}     

            self.STATIONS_BLOCKS = {
                "Pioneer": 2,
                "Edgebrook": 9,
                "Station": 16,
                "Whited": 22,
                "South Bank": 31,
                "Central-I": 39,
                "Inglewood-I": 48,
                "Overbrook-I": 57,
                "Glenbury-K": 65,
                "Dormont-N": 73,
                "Mt. Lebanon": 77,
                "Poplar": 88,
                "Castle Shannon": 96,
                "Dormont-T": 105,
                "Glenbury-U": 114,
                "Overbrook-W": 123,
                "Inglewood-W": 132,
                "Central-W": 141,
                "Yard": 152 
            }
        #elif name == "Red":
        #    self.entrance_blocks = [1, 2, 3] #Entrance blocks for red line
        else:
            print("ERROR: Track name not recognized. Please use 'Green'.") # "or 'Red'"

        self.initialize_blocks()

    def initialize_blocks(self):
        self.blocks = [TrackBlocks(block) for block in self.track_data.blocks]

    def add_train_data(self, train_id, train_route, train_mode, start_block):
        #Adds train to active trains list
        new_train = DummyTrain(train_id, train_route, train_mode, start_block)
        self.current_trains.append(new_train) 
        

    def add_train_object(self, train_object):
        #Adds train object to active trains list
        self.current_trains.append(train_object)
        

    def get_train_data(self, train_id):
        if train_id not in self.current_trains:
            return None
        else:
            return self.current_trains[train_id]