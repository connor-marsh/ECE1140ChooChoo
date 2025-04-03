'''
Author: Aaron Kuchta
Date: 4-1-2025
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
        self.route_data = {}

        #Controls active track data
        self.green_line = Track("Green")
        #self.red_line = Track("Red") #No red line implementation yet
        self.active_line = self.green_line

        self.train_queue = queue.Queue()

        self.wall_clock = global_clock.clock

        #Read in signal from Track Model
        signals.communication.track_tickets.connect(self.update_tickets)  #int
        signals.communication.wayside_block_occupancies.connect(self.update_occupancy) #List
        signals.communication.wayside_switches.connect(self.update_switches) #List
        signals.communication.wayside_lights.connect(self.update_lights) #List
        signals.communication.wayside_crossings.connect(self.update_crossings) #List
        
        
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

        

    def backend_update(self):
        if self.wall_clock.minute != self.last_minute:
            self.elapsed_mins += 1
            self.last_minute = self.wall_clock.minute
        #print("Elapsed Time", self.elapsed_mins)
        self.dispatch_queue_handler() #Dispatch queue handler    
        if self.active_line.blocks[62].occupancy:
            self.suggested_speed = {"K63" : 70}
            self.suggested_authority = {"K63" : 16134}
            self.send_suggestions(self.suggested_speed, self.suggested_authority) #Send suggestions to wayside  
        if self.active_line.blocks[9].occupancy:
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
        for index, row in file_data.iterrows():
            if row['Designation'] != "":
                designation = row['Designation']
                total_stops = row['Total # of Stops']
                all_stops = [int(stop) for stop in row.iloc[2:].dropna().tolist()]

                self.route_data[index] = {
                    'designation': designation,
                    'num_stops': total_stops,
                    'listed_stops': all_stops
                }

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

    @pyqtSlot(list)
    def update_occupancy(self, occupancy_list):
        #Updates occupancy list | called by wayside controller
        for block_id, occupancy in zip(self.active_line.blocks, occupancy_list):
            self.active_line.blocks[block_id].occupancy = occupancy

    @pyqtSlot(list)
    def update_switches(self, switch_list):
        self.active_line.switch_states = switch_list

    @pyqtSlot(list)
    def update_lights(self, light_list):
        #Updates light list | called by wayside controller
        self.active_line.lights = light_list
            
    @pyqtSlot(list)
    def update_crossings(self, crossing_list):
        self.active_line.crossings = crossing_list

    def first_blocks_free(self):
        #Checks if first blocks are free | called by dispatch queue handler
        block_1 = self.active_line.blocks[self.active_line.ENTRANCE_BLOCK].occupancy 

        if not block_1: #Check correctness of this logic
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
        #Handles train queue | called by update function
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
        print("TRAIN DISPATCHED")

    def send_block_maintenance(self, block_id, maintenance_val):
        signals.communication.ctc_block_maintenance.emit(block_id, maintenance_val) #int, bool 
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

    
class DummyTrain:
    def __init__(self, train_id, route, mode):
        super().__init__()
        self.train_id = train_id
        self.route = route
        self.mode = mode
        self.current_block = 62 #Starting block for green line
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
        self.suggested_speed = 0
        self.suggested_authority = 0
        self.updated = True
        #May need addition values
        #print("Block ID: ", self.id, "Switch", self.has_switch) #Testing line, remove later

class Track: 
    def __init__(self, name):
        self.track_data = global_track_data.lines[name]
        self.name = name
        self.active_trains = []
        self.blocks = []
        self.switch_data = self.track_data.switches.copy()
        self.station_names = self.track_data.stations.copy()
        self.switch_states = [0,0,0,0,0,0] #hardcoded
        self.lights = [0,0,0,0,0,0] #hardcoded
        self.crossings = [0,0] #hardcoded

        if name == "Green":
            self.ENTRANCE_BLOCK = 1  #Entrance blocks for green line | Now unique
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