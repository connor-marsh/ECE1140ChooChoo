'''
Author: Aaron Kuchta
Date: 3-30-2025
'''


import sys
import os
import time
import queue 
import pandas as pd
import openpyxl 
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
import globals.global_clock as global_clock




class TestBenchFrontEnd:
    def __init__(self, ctc_app):
        super().__init__()
        self.ctc_tb_ui = CtcTestBenchUI()
        self.ctc_tb_ui.setupUi(self)

        self.ctc_app = ctc_app

        self.ctc_tb_ui.tb_in_confirm_vals.clicked.connect(self.read_test_bench_data)

    def read_test_bench_data(self):
        #Variables initialization
        block_states = []#0 unoccupied, 1 occupied, 2 failure
        railway_crossing_states = []#0 open, 1 closed
        light_states = []#0 green, 1 yellow, 2 red
        switch_states = []#0 left, 1 right

        #Read data from test bench
        block_input = self.ctc_tb_ui.tb_in_block_states.toPlainText().strip()
        crossing_input = self.ctc_tb_ui.tb_in_crossing_states.toPlainText().strip()
        light_input = self.ctc_tb_ui.tb_in_light_states.toPlainText().strip()
        switch_input = self.ctc_tb_ui.tb_in_switch_states.toPlainText().strip()

        if block_input:
            block_states = [int(x) for x in block_input.split(",")]
            #print(f"Block input: {block_states}") #debugging statment
        if crossing_input:
            railway_crossing_states = [int(x) for x in crossing_input.split(",")]
        if light_input:
            light_states = [int(x) for x in light_input.split(",")]
        if switch_input:
            switch_states = [int(x) for x in switch_input.split(",")]

        self.ctc_app.get_test_bench_data(block_states, railway_crossing_states, light_states, switch_states)  

    def print_suggested_speed(self, speed):
        self.ctc_tb_ui.tb_out_speed.setText(speed)

    def print_suggested_authority(self, auth):
        self.ctc_tb_ui.tb_out_authority.setText(auth)
    
    def print_maintenance(self, block_id, maintenance_val):
        message = ("Block " + str(block_id) + ": " + str(maintenance_val))
        self.ctc_tb_ui.tb_out_maintenance.setText(message)

    def print_switch_state(self, block_id, switch_state):
        message = ("Block " + str(block_id) + ": " + str(switch_state))
        self.ctc_tb_ui.tb_out_switch_states.setText(message)

class CtcFrontEnd(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.ctc_ui = CtcUI()
        self.ctc_ui.setupUi(self)
        self.backend = backend #Establishes backrend refrence
        #self.backend.link_frontend(self)

        #Variable initializations
        self.active_block_id = ""
        self.active_block_length = ""
        self.active_block_speed = ""

        # Connect buttons
        self.ctc_ui.main_switch_to_dispatch_button.clicked.connect(self.switch_to_dispatch_page)
        self.ctc_ui.main_switch_to_select_button.clicked.connect(self.switch_to_select_page)
        self.ctc_ui.main_switch_to_maintenance_button.clicked.connect(self.switch_to_maintenance_page)
        self.ctc_ui.sub_return_button.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button2.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button3.clicked.connect(self.switch_to_home)

        self.ctc_ui.main_switch_to_upload_button.clicked.connect(self.get_train_schedule)
        #self.ctc_ui.main_upload_map_button.clicked.connect(self.get_map_data)

        self.ctc_ui.maintenance_toggle.clicked.connect(self.toggle_maintenance_mode)
        #self.ctc_ui.main_map_table.cellClicked.connect(self.on_map_row_clicked)
        #self.ctc_ui.main_line_slider.sliderReleased.connect(self.toggle_active_line) #Not implemented yet
        self.ctc_ui.main_switch_knob.valueChanged.connect(self.set_switch_state)
        #self.ctc_ui.sub_confirm_override_button.clicked.connect(self.update_suggested)
        #self.ctc_ui.sub_activate_maintenance_button.clicked.connect(self.start_maintenance)
        #self.ctc_ui.sub_end_maintenance_button.clicked.connect(self.end_maintenance)
        self.ctc_ui.sub_dispatch_confirm_button.clicked.connect(self.dispatch_pressed)
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)# Set Starting page for stacked widget
        #self.toggle_mode() #toggles manual mode, NEEDS CHANGED 

        self.toggle_maintenance_mode()
        self.initialize_map()
        self.initialize_block_combo()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.frontend_update)
        self.timer.start(100)  # 10 Hz update - change to slower update for performance??

        self.wall_clock = global_clock.clock

    def frontend_update(self):
        self.update_clock() #update clock label
        self.update_throughput() #update throughput label
        self.update_track_table() #update track data table


    #Stacked Widget Navigation
    def switch_to_dispatch_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(1)

    def switch_to_select_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(2)

    def switch_to_maintenance_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(3)

    def switch_to_home(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)

    def open_file_dialog(self):
        # Opens file dialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel Files (*.xlsx)')

        if not file_name:
            return None  # If no file is selected, return None
            
        file_data = pd.read_excel(file_name)
        return file_data
    
    def get_train_schedule(self):
        #open file dialog
        route_schedules = self.open_file_dialog()
        self.backend.process_route_data(route_schedules)

    def on_map_row_clicked(self, row, column):
        #stores data for clicked block
        self.selected_row = row+1 #Stores for later use
        block_info = self.block_data.get(row+1)
        self.update_block_data_labels(block_info)

    def update_block_data_labels(self,block_info):
        #update block id, length, speed limit | on main page as well as maintenance page
        self.ctc_ui.main_active_block_id.setText(str(block_info['block_id']))
        self.ctc_ui.sub_active_block_id.setText(str(block_info['block_id']))
        self.ctc_ui.main_active_block_length.setText(str(block_info['block_length']))
        self.ctc_ui.main_active_block_speed_limit.setText(str(block_info['speed_limit']))

    def update_clock(self):
        #Main UI clock element
        clock_time = self.global_clock.text()
        day_night = self.global_clock.am_pm()
        full_time = clock_time + " " + day_night
        self.ctc_ui.current_time_label.setText(full_time)

    def initialize_block_combo(self):
        #initialize block combo box with block ids - currently 1-150
        self.ctc_ui.sub_block_number_combo.clear()
        for i in range(1, 150):
            self.ctc_ui.sub_block_number_combo.addItem(str(i))

    #Map Ini - OVERHAUL NEEDED - TRACK CLASS UPDATED
    def initialize_map(self):
        self.block_data = self.backend.get_blocks()
        #update map with block data
        self.ctc_ui.main_map_table.setRowCount(len(self.block_data))

        for row_index, (block_id, block_info) in enumerate(self.block_data.items()): 
            #If cell doesnt not have value for column, set color to black, 

            self.ctc_ui.main_map_table.setItem(row_index, 0, QTableWidgetItem(str(block_info['section'])))
            self.ctc_ui.main_map_table.setItem(row_index, 1, QTableWidgetItem(str(block_info['block_id'])))

            occupancy_item = QTableWidgetItem()
            occupancy_item.setBackground(QColor("green"))
            self.ctc_ui.main_map_table.setItem(row_index, 2, occupancy_item)

            station_item = QTableWidgetItem(str(block_info['station']))
            if block_info['station'] == " ":
                station_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 3, station_item)

            switch_item = QTableWidgetItem(str(block_info['switch']))
            if block_info['switch'] == " ":
                switch_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 4, switch_item)

            traffic_light_item = QTableWidgetItem("")
            if block_info['traffic_light']:
                traffic_light_item.setBackground(QColor("green"))
            else:
                traffic_light_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 5, traffic_light_item)

            crossing_item = QTableWidgetItem("")
            if block_info['crossing']:
                crossing_item.setBackground(QColor("green"))
            else:
                crossing_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 6, crossing_item)

            maintenance_item = QTableWidgetItem()
            maintenance_item.setBackground(QColor("white"))
            self.ctc_ui.main_map_table.setItem(row_index, 7, maintenance_item)

            transponder_item = QTableWidgetItem("")
            if block_info['transponder']:
                transponder_item.setBackground(QColor("green"))
            else:
                transponder_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 8, transponder_item)

            underground_item = QTableWidgetItem("")
            if block_info['underground']:
                underground_item.setBackground(QColor("green"))
            else:
                underground_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 9, underground_item)

        self.ctc_ui.main_map_table.resizeColumnsToContents()

    def update_map(self):
        #updates map occupancy, maintenance, switch state, crossing state and light color
        pass

    def update_throughput(self):
        #updates throughput label on UI
        self.ctc_ui.main_throughput_label.setText(str(self.backend.throughput))

    def dispatch_pressed(self):
        if self.ctc_ui.sub_dispatch_overide_new_radio.isChecked():
            #new train needs to be dispatched
            if self.ctc_ui.sub_dispatch_station_select_radio.isChecked():
                #dispatch to station
                destination_station = self.ctc_ui.sub_station_combo.currentIndex()
                self.backend.dispatch_handler(destination_station, 'station')
            elif self.ctc_ui.sub_dispatch_block_select_radio.isChecked():
                #dispatch to block
                destination_block = self.ctc_ui.sub_block_number_combo.currentText()
                self.backend.dispatch_handler(destination_block, 'block')
            #elif For selected route from table | not implemented yet
        elif self.ctc_ui.sub_dispatch_overide_existing_radio.isChecked():
            #existing train needs to be rerouted | not implemented yet
            print("Reroute Train Not Implemented")

    #maintenance page - Change to send data to backend - UPDATE NEEDED, TRACK CLASS CHANGED
    def start_maintenance(self):
        #starts maintenance on selected block | activated by button
        if self.selected_row is not None:
            block_info = self.block_data.get(self.selected_row)
            block_info['maintenance'] = 1
            self.update_maintenance(block_info)
            self.backend.send_maintenance(block_info['block_id'], 1) #Calls backend to send data to wayside
            self.test_bench.print_maintenance(block_info['block_id'], 1)
        
    def end_maintenance(self):
        #ends maintenance on selected block | activated by button 
        if self.selected_row is not None:
            block_info = self.block_data.get(self.selected_row)
            block_info['maintenance'] = 0
            self.update_maintenance(block_info)
            self.backend.send_maintenance(block_info['block_id'], 0) #Calls backend to send data to wayside
            self.test_bench.print_maintenance(block_info['block_id'], 0)
    
    def update_maintenance(self, block_info):
        #updates maintenance mode | activated by button
        case = block_info['maintenance']
        if case == 0:
            self.ctc_ui.main_map_table.item(block_info['block_id']-1, 7).setBackground(QColor("white"))
        elif case == 1:
            self.ctc_ui.main_map_table.item(block_info['block_id']-1, 7).setBackground(QColor("red"))
    
    def toggle_maintenance_mode(self):
        if self.ctc_ui.maintenance_toggle.isChecked():
            self.ctc_ui.main_switch_knob.setEnabled(True)
            self.ctc_ui.sub_activate_maintenance_button.setEnabled(True)
            self.ctc_ui.sub_end_maintenance_button.setEnabled(True)

        else:
            self.ctc_ui.main_switch_knob.setEnabled(False)
            self.ctc_ui.sub_activate_maintenance_button.setEnabled(False)
            self.ctc_ui.sub_end_maintenance_button.setEnabled(False)
            self.ctc_ui.main_switch_knob.setSliderPosition(1)
        
    def set_switch_state(self):
        #updates switch state | activated by knob
        switch_state = self.ctc_ui.main_switch_knob.value()
        if self.selected_row is not None: # and block has switch
            #set block switch value
            self.backend.send_switch_states(block_id, switch_state)


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
        self.trackModel.track_tickets.connect(self.tickets_handler()) #need to specify param?
        
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
        return self.active_line.blocks

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



    def tickets_handler(self, num_tickets):
        #Takes tickets sold from track model and updates throughput
        self.total_tickets += num_tickets
        self.throughput = self.total_tickets / (self.elapsed_mins/60) #Tickets per hour
        #Send throughput to UI
        self.frontend.update_throughput(self.throughput)

    def first_blocks_free(self):
        #Checks if first blocks are free | called by dispatch queue handler
        block_1 = self.active_line.blocks[self.active_line.entrance_blocks[0]] 
        block_2 = self.active_line.blocks[self.active_line.entrance_blocks[1]]
        block_3 = self.active_line.blocks[self.active_line.entrance_blocks[2]]

        if block_1['occupancy'] == 0 and block_2['occupancy'] == 0 and block_3['occupancy'] == 0: #Needs updated after new track class implemented
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
        #ctc_dispatch.emit()
        pass

    def send_maintenance(self, block_id, maintenance_val):
        #ctc_maintenance.emit(block_id, maintenance_val)
        pass

    def send_suggestions(self, suggested_speeds, suggested_authorities):
        #ctc_suggested.emit(suggested_speeds, suggested_authorities)
        pass

    def send_exit_blocks(self, exit_blocks):
        #ctc_exit_blocks.emit(EDGEBROOK_EXIT_BLOCKS[0], EDGEBROOK_EXIT_BLOCKS[1], EDGEBROOK_EXIT_BLOCKS[2])
        pass

    def send_switch_states():
        #ctc_switch_states.emit(switchStates)
        pass

    
class Track: 

    GREEN_LINE = 'testTrack_v1.xlsx'
    #RED_LINE = 'testTrack_red.xlsx'

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.file_name = ''
        self.blocks = {}
        self.active_trains = {}

        if name == "Green":
            self.file_name = Track.GREEN_LINE
            self.entrance_blocks = [62, 63, 64] #Entrance blocks for green line
        #elif name == "Red":
        #    self.file_name = Track.RED_LINE
        #    self.entrance_blocks = [1, 2, 3] #Entrance blocks for red line
        else:
            print("ERROR: Track name not recognized. Please use 'Green' or 'Red'.")


        self.initialize_blocks()



    def initialize_blocks(self):
        
        file_data = pd.read_excel(self.file_name)
        for index, row in file_data.iterrows():
            block_section = row['Section']
            block_id = int(row['Block Number'])
            block_length = int(row['Block Length (m)'])
            block_speed_limit = int(row['Speed Limit (Km/Hr)'])
            block_station = row['Station'] if isinstance(row['Station'], str) else " "
            block_switch = row['Switch'][7:] if isinstance(row['Switch'], str) else " " #remove "Switch " from string - MAY NEED UPDATED
            block_crossing = 1 if pd.notna(row['Crossing']) else 0
            block_traffic_light = 1 if pd.notna(row['Light']) else 0
            block_transponder = 1 if pd.notna(row['Transponder']) else 0
            block_underground = 1 if pd.notna(row['Underground']) else 0

            #set default values for crossing and light
            crossing_active = 0 #0 open, 1 closed
            light_color = 0 #0 green, 1 red
            occupancy = 0 #0 unoccupied, 1 occupied, 2 failure | TO CHANGE
            switch_state = 0 #0 left, 1 right
            maintenance = 0 #0 no maintenance, 1 maintenance 

            self.blocks[block_id] = {
                'section': block_section,
                'block_id': block_id,
                'occupancy': occupancy,
                'maintenance': maintenance,
                'block_length': block_length,
                'speed_limit': block_speed_limit,
                'station': block_station,
                'station_side': 'L', #UPDATE NEEDED ON XLXS
                'switch': block_switch,
                'switch_state': switch_state,
                'crossing': block_crossing,
                'crossing_active': crossing_active,
                'traffic_light': block_traffic_light,
                'light_color': light_color,
                'transponder': block_transponder,
                'underground': block_underground
            }



    def set_block_occupancy(self, block_id, occupancy):
        #sets occupancy for block
        if block_id in self.blocks:
            self.blocks[block_id]['occupancy'] = occupancy
        else:
            print(f"CTC Set Occupancy ERROR! Block ID {block_id} not found.")

    def set_block_maintenance(self, block_id, maintenance_val):
        #sets maintenance for block
        if block_id in self.blocks:
            self.blocks[block_id]['maintenance'] = maintenance_val
        else:
            print(f"CTC Set Maintenance ERROR! Block ID {block_id} not found.")

    def set_block_switch_state(self, block_id, switch_state):
        #sets switch state for block
        if block_id in self.blocks:
            self.blocks[block_id]['switch_state'] = switch_state
        else:
            print(f"CTC Set Switch ERROR! Block ID {block_id} not found.")

    def set_block_light_state(self, block_id, light_color):
        #sets light state for block
        if block_id in self.blocks:
            self.blocks[block_id]['light_color'] = light_color
        else:
            print(f"CTC Set Light ERROR! Block ID {block_id} not found.")

    def set_block_crossing_state(self, block_id, crossing_state):
        #sets crossing state for block
        if block_id in self.blocks:
            self.blocks[block_id]['crossing_active'] = crossing_state
        else:
            print(f"CTC Set Crossing ERROR! Block ID {block_id} not found.")

    def get_block_data(self, block_id):
        #Returns block data for given block id
        if block_id in self.blocks:
            return self.blocks[block_id]
        else:
            return None

    def add_active_train(self, train_id, train_route, train_mode):
        #Adds train to active trains list
        self.active_trains[train_id] = {
            'train_id': train_id,
            'route': train_route,
            'next_stop': train_route, #Change so it is the next stop, not the whole route----------
            'mode': train_mode,
            'curent_block': None,
            'authority': None}
            #add exit blocks, authority, speed, etc.
        

    def get_train_data(self, train_id):
        if train_id not in self.active_trains:
            return None
        else:
            return self.active_trains[train_id]


            
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

def main():
    app = QApplication(sys.argv)
    
    backend = CtcBackEnd()
    ctc_app = CtcFrontEnd(backend)


    ctc_app.show()
    #ctc_app.test_bench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()