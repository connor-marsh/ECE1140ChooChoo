'''
Author: Aaron Kuchta
Date: 4-7-2025
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

    #Stations located green line
    G_STATIONS = ("Pioneer", "Edgebrook", "Station", "Whited", "South Bank", "Central", "Inglewood", "Overbrook", "Glenbury", "Dormont", 
                "MT Lebanon", "Poplar", "Castle Shannon", "Dormont", "Glenbury", "Overbrook", "Inglewood", "Central")
    G_STATIONS_BLOCKS = (2, 9, 16, 22, 31, 39, 48, 57, 65, 73, 77, 88, 96, 105, 114, 123, 132, 141)

    EDGEBROOK_EXIT_BLOCKS = [[0,0,1], [0,0,1], [0,0,1]] #1 hot vector for each wayside exit blocks - Need to find which blocks
    
    #Stations located on red line
    #R_STATIONS = ()
    #R_STATIONS_BLOCKS = ()

    def __init__(self): 
        super().__init__()
        self.sent62 = False # These are temporary fixes that allow the ctc to only send authorities/speeds one time per occupancy update
        self.sent9 = False
        self.routes = {}

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
        self.train_count = 0
        self.elapsed_mins = 0
        self.last_minute = self.wall_clock.minute

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.backend_update)
        self.timer.start(100)  # 10 Hz update
        self.calculate_authority(12, 150, 0) #Test function, remove later

        

    def backend_update(self):
        if self.wall_clock.minute != self.last_minute:
            self.elapsed_mins += 1
            self.last_minute = self.wall_clock.minute
        #print("Elapsed Time", self.elapsed_mins)
        self.dispatch_queue_handler() #Dispatch queue handler  

        if self.active_line.blocks[62].occupancy:
            self.suggested_speed = {"K63" : 70}
            self.suggested_authority = {"K63" : 16134}
            print("In ctc dispatch")
            self.send_suggestions(self.suggested_speed, self.suggested_authority) #Send suggestions to wayside
        if self.active_line.blocks[8].occupancy:
            self.suggested_speed = {"C9" : 45}
            self.suggested_authority = {"C9" : 5959}
            self.send_suggestions(self.suggested_speed, self.suggested_authority) #Send suggestions to wayside 


            
        
    def get_map_data(self):
        return self.active_line.blocks, self.active_line.station_names, self.active_line.switch_data, self.active_line.switch_states, self.active_line.lights, self.active_line.crossings

    def process_route_data(self, file_data):
        if(file_data is not None):
            self.read_route_file(file_data)
            self.initialize_route_table()   

    def read_route_file(self, file_data):
        for _, row in file_data.iterrows():
            route_name = row.iloc[0]
            stations = row[1:].dropna().tolist()
            self.routes[route_name] = stations

        #for route, stations in self.routes.items(): #Debug info
        #    print(f"{route}: {', '.join(stations)}")

    def initialize_route_table(self):

        pass

    def upload_train_schedule(self):
        #uploads train schedule file | activated by button
        pass

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

    


    def update_train_location(self, occupancy_list):
        if len(self.active_line.active_trains) != 0:
            for i in occupancy_list:
                if occupancy_list[i] == 1: # HARDCODED, BUT NOT KEY
                    self.active_line.active_trains[0].current_block = i
                        

    def first_blocks_free(self):
        #Checks if first blocks are free | called by dispatch queue handler
        block_1 = self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].occupancy or self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].maintenance
        #print("Block ", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].id, "Occupancy is", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].occupancy, " and has maintenance ", self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].maintenance)
        if not block_1: # Altered from 3 blocks
            return True
        else:
            return False

    def dispatch_handler(self, destination, destination_type):
        #Train dispatch handler | called by front end
        if destination_type == 'station':
            #Dispatch to station
            destination_block = int(self.G_STATIONS_BLOCKS[destination])
            print("Trying to dispatch to: ", destination, " Block: ", self.G_STATIONS_BLOCKS[destination])
        elif destination_type == 'block':
            #Dispatch to block
            destination_block = int(destination)
            print("Trying to dispatch to block", destination)

        self.train_queue.put(destination_block)
        print("Train Entered into Queue")

    def dispatch_queue_handler(self):
        # Handles train queue | called by update function
        if not self.train_queue.empty() and self.first_blocks_free():
            #get destination block from queue
            destination_block = self.train_queue.get()
            self.active_line.add_active_train(self.train_count, destination_block, "manual")
            self.train_count += 1
            #Update active train list
            print("Train Leaving Queue")
            self.send_dispatch_train() 
 
    def send_dispatch_train(self):
        signals.communication.ctc_dispatch.emit() # Just signal, no param
        print("Train Dispatched from CTC")

    def send_block_maintenance(self, block_id, maintenance_val):
        signals.communication.ctc_block_maintenance.emit(self.active_line.blocks[block_id].id, maintenance_val) #int, bool 
        print("Set Block ", block_id, " Maintenance value to ", maintenance_val)
        print("Stored Block value: ", self.active_line.blocks[block_id].id, " ", self.active_line.blocks[block_id].maintenance)

    def send_suggestions(self, suggested_speeds, suggested_authorities): 
        signals.communication.ctc_suggested.emit(suggested_speeds, suggested_authorities) #Dict, Dict

    def send_exit_blocks(self, exit_blocks):
        signals.communication.ctc_exit_blocks.emit() #List, Currently Unused

    def send_switch_states(self, block_id, switch_state): #KNOWN ERROR - SENDS SWITCH VAL WHEN EXITING MAINTENANCE
        switch_id = self.active_line.blocks[block_id].id
        signals.communication.ctc_switch_maintenance.emit(switch_id, switch_state) #String, bool
        print("Switch on Block ", switch_id, " set to ", switch_state)

    
    def calculate_authority(self, start_id, end_id, direction=1):
        '''
        Parameters:
            start_id: The block ID to start from (1-150)
            end_id: The block ID to end on (1-150)
            direction: Starting movment direction, 0 for decreasing, 1 for increasing

        Returns: 
            Authority needed to reach end from start
    
        TODO:
            - Adapt for red line
            - Adapt for yard entrance/exit blocks
        '''
        start_id = start_id - 1 #Convert to 0-indexed
        end_id = end_id - 1 #Convert to 0-indexed
        current_id = start_id
        
        if start_id == end_id:
            return 0
        if start_id < 0 or start_id > 149:
            print("Invalid start block ID")
            return -1
        
        authority = 0
        last_dir = direction #Initial direction
        section_dir = self.active_line.sections[self.active_line.blocks[start_id].id[0]].increasing #0 for decreasing, 1 for increasing, 2 for bidirectional
        #print("Block: ", self.active_line.blocks[start_id].id, "Direction: ", section_dir)

        while current_id != end_id:
            current_block = self.active_line.blocks[current_id]
            section_key = current_block.id[0]  #Gets section letter
            #section_dir = self.active_line.sections[section_key].increasing

            jump_key = (current_id+1, direction)
            #print("Current Block: ", current_block.id, "Direction: ", direction, "Jump Key: ", jump_key)

            if jump_key in self.active_line.JUMP_BLOCKS:
                #print("JUMP BLOCK DETECTED - ", current_block.id, "Direction: ", direction, "Jump Key: ", jump_key)
                next_id, new_dir = self.active_line.JUMP_BLOCKS[jump_key]
                next_dir = new_dir
            elif direction == 0:
                next_id = current_id - 1
                if next_id < 0:
                    print("JUMP BLOCK MISSED 1-13")
                next_dir = direction
            elif direction == 1:
                next_id = current_id + 1
                if next_id >= 150:
                    print("JUMP BLOCK MISSED 150-28")
                next_dir = direction

            authority += current_block.length #accumulate authority
            #print("Current Block: ", self.active_line.blocks[current_id].id, "Next Block: ", self.active_line.blocks[next_id].id, "Direction: ", direction, "Total Authority: ", authority)

            current_id = next_id #Update current block
            direction = next_dir

        current_block = self.active_line.blocks[current_id] 
        authority += current_block.length

        #print("-----END REACHED-----")
        #print("Current Block: ", current_block.id, "Total Authority: ", authority)
        return authority


class DummyTrain:
    def __init__(self, train_id, route, mode):
        super().__init__()
        self.train_id = train_id
        self.route = route
        self.mode = mode
        self.current_block = 64 #Starting block for green line
        self.speed = 0
        self.authority = 0

    def set_current_block(self, block_id):
        self.current_block = block_id

    def set_authority(self, authority):
        self.authority = authority
    
    def set_mode(self, mode):
        self.mode = mode

    def set_route(self, route):
        self.route = route

    
class TrackBlocks:
    def __init__(self, block):
        self.id = block.id
        self.length = block.length #IN YARDS, UPDATE UI-------------------------------
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
        #May need addition values
        #print("Block ID: ", self.id, "Switch", self.has_switch) #Testing line, remove later

class Track: 
    def __init__(self, name):
        self.JUMP_BLOCKS = { 
            (100, 1): (84, 0),   # Q100 -> N85, decrease
            (77, 0): (100, 1),   # N77 -> R101, increase
            (150, 1): (27, 0),   # Z150 -> F28, decrease
            (1, 0): (12, 1)}     #A1 -> D13, increase
            #More may be needed for Yard Entrace/exit
        self.track_data = global_track_data.lines[name]
        self.name = name
        self.active_trains = []
        self.blocks = []
        self.sections = self.track_data.sections
        #print("Sections: ", self.sections)
        self.switch_data = self.track_data.switches
        self.station_names = self.track_data.stations.copy()
        self.switch_states = [0,0,0,0,0,0] #hardcoded
        self.lights = [0,0,0,0,0,0] #hardcoded
        self.crossings = [0,0] #hardcoded

        if name == "Green":
            self.ENTRANCE_BLOCK = 62  #Entrance blocks for green line | Should be K63 but is 62 to account for 0-indexing
        #elif name == "Red":
        #    self.entrance_blocks = [1, 2, 3] #Entrance blocks for red line
        else:
            print("ERROR: Track name not recognized. Please use 'Green'.") # "or 'Red'"

        self.initialize_blocks()

    def initialize_blocks(self):
        self.blocks = [TrackBlocks(block) for block in self.track_data.blocks]

    def add_active_train(self, train_id, train_route, train_mode="manual"):
        #Adds train to active trains list
        new_train = DummyTrain(train_id, train_route, train_mode)
        self.active_trains.append(new_train) #Changed to list, was dictionary
        

    def get_train_data(self, train_id):
        if train_id not in self.active_trains:
            return None
        else:
            return self.active_trains[train_id]