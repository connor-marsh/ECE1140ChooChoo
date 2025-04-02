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
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
import globals.global_clock as global_clock
import globals.track_data_class as track_data
import globals.signals as signals


class CtcBackEnd():

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
        signals.track_tickets.connect(self.update_tickets)  #int

        signals.wayside_block_occupancies.connect(self.update_occupancy) #List
        signals.wayside_switches.connect(self.update_switches()) #List
        signals.wayside_lights.connect(self.update_lights()) #List
        signals.wayside_crossings.connect(self.update_crossings()) #List
        
        
        self.suggested_speed = [] #length of track, each block has a suggested speed, speed limit for now
        self.suggested_authority = [] #length of track, each block has a suggested authority, -1 for no change
        self.manual_switch_states = [] #length of switch count, each block has a switch state, 0 for first option, 1 for second option

        self.total_tickets = 0
        self.throughput = 0
        self.train_count = 0
        self.elapsed_mins = 0
        self.last_minute = self.wall_clock.get_minute()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.backend_update)
        self.timer.start(100)  # 10 Hz update

        

    def backend_update(self):
        if self.wall_clock.get_minute() != self.last_minute:
            self.elapsed_mins += 1
            self.last_minute = self.wall_clock.get_minute()

        self.dispatch_queue_handler() #Dispatch queue handler    
        self.send_suggestions() #Send suggestions to wayside     
        
    def get_blocks(self):
        return self.active_line.blocks, self.active_line.switches 

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


    def update_active_trains_count(self):
        #Updated mainscreen train count
        #reads number of rows from train data file + manual sent trains
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
        #Send throughput to UI
        self.frontend.update_throughput(self.throughput)

    @pyqtSlot(list)
    def update_occupancy(self, occupancy_list):
        #Updates occupancy list | called by wayside controller
        for block_id, occupancy in zip(self.active_line.blocks.keys(), occupancy_list):
            self.active_line.blocks[block_id].occupancy = occupancy
        

    @pyqtSlot(list)
    def update_switches(self, switch_list):
        pass

    @pyqtSlot(list)
    def update_lights(self, light_list):
        pass

    @pyqtSlot(list)
    def update_crossings(self, block_id, crossing_state):
        pass

    def first_blocks_free(self):
        #Checks if first blocks are free | called by dispatch queue handler
        block_1 = self.active_line.blocks[self.active_line.entrance_blocks[0]].occupancy 
        block_2 = self.active_line.blocks[self.active_line.entrance_blocks[1]].occupancy
        block_3 = self.active_line.blocks[self.active_line.entrance_blocks[2]].occupancy

        if not block_1 and not block_2 and not block_3: #Check correctness of this logic
            return True
        else:
            return False

    def dispatch_handler(self, destination, destination_type):
        #Train dispatch handler | called by front end
        if destination_type == 'station':
            #Dispatch to station
            destination_block = int(self.G_STATION_BLOCKS[destination])
        elif destination_type == 'block':
            #Dispatch to block
            destination_block = int(destination)

        self.train_queue.put(destination_block)

    def dispatch_queue_handler(self):
        #Handles train queue | called by update function
        if not self.train_queue.empty() and self.first_blocks_free():
            #get destination block from queue
            destination_block = self.train_queue.get()
            Track.add_active_train(self.train_count, destination_block, "manual")
            self.train_count += 1
            self.update_active_trains_count() #Move to own function eventually, update periodicly
            #Update active train list
            self.send_dispatch_train() 
 
    def send_dispatch_train(self):
        signals.ctc_dispatch.emit() # Just signal, no param

    def send_block_maintenance(self, block_id, maintenance_val):
        signals.ctc_block_maintenance.emit(block_id, maintenance_val) #int, bool | should be string, bool??? ASK CONNOR

    def send_suggestions(self, suggested_speeds, suggested_authorities):
        signals.ctc_suggested.emit(suggested_speeds, suggested_authorities) #List, List

    def send_exit_blocks(self, exit_blocks):
        signals.ctc_exit_blocks.emit() #List, Currently Unused

    def send_switch_states(self, switch_id, switch_state):
        switch_id = "0" #String to locate switch
        switch_state = False #False for first option, True for second option
        signals.ctc_switch_maintenance.emit(switch_id, switch_state) #String, bool

    
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
        self.suggested_speed = 0
        self.suggested_authority = 0
        self.updated = True
        #May need addition values
        print("Block ID: ", self.id) #Testing line, remove later

class Track: 
    def __init__(self, name):
        self.name = name
        self.active_trains = {}
        self.blocks = []
        self.switches = track_data.track_data.switches.copy()
        self.lights = track_data.track_data.lights.copy()
        #self.crossings = track_data.track_data.crossings.copy()

        if name == "Green":
            self.entrance_blocks = ["J62", "K63", "K64"] #Entrance blocks for green line
        #elif name == "Red":
        #    self.entrance_blocks = [1, 2, 3] #Entrance blocks for red line
        else:
            print("ERROR: Track name not recognized. Please use 'Green'.") # "or 'Red'"

        self.initialize_blocks()

    def initialize_blocks(self):
        self.blocks = [TrackBlocks(block) for block in track_data.track_data.blocks]

    def add_active_train(self, train_id, train_route, train_mode):
        #Adds train to active trains list
        new_train = DummyTrain(train_id, train_route, train_mode)
        self.active_trains[train_id] = new_train
        

    def get_train_data(self, train_id):
        if train_id not in self.active_trains:
            return None
        else:
            return self.active_trains[train_id]