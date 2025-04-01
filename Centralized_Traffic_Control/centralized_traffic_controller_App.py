'''
Author: Aaron Kuchta
Date: 3-30-2025
Version: 2.0
'''


import sys
import os
import time
import pandas as pd
import openpyxl 
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
#import globals.global_clock as global_clock




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

class WaysideSignal:
    pass




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
        #self.ctc_ui.main_switch_knob.valueChanged.connect(self.set_switch_state)
        #self.ctc_ui.sub_confirm_override_button.clicked.connect(self.update_override)
        #self.ctc_ui.sub_activate_maintenance_button.clicked.connect(self.start_maintenance)
        #self.ctc_ui.sub_end_maintenance_button.clicked.connect(self.end_maintenance)
        self.ctc_ui.sub_dispatch_confirm_button.clicked.connect(self.dispatch_pressed)
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)# Set Starting page for stacked widget
        #self.toggle_mode() #toggles manual mode, NEEDS CHANGED 

        self.toggle_maintenance_mode()
        self.initialize_map()


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


    #Map Ini - UPDATE NEEDED, SWITCH DIRECTION
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

    def update_occupancy_map(self, occupancy):
        pass
    def update_switch_map(self, state):
        pass
    def update_light_map(self, state):
        pass
    def update_crossing_map(self, state):
        pass
    def update_maintenance_map(self, state):
        pass

    def update_throughput(self, throughput):
        #updates throughput label on main screen
        self.ctc_ui.main_throughput_label.setText(str(throughput))

    def dispatch_pressed(self):
        if self.ctc_ui.sub_dispatch_overide_new_radio.isChecked():
            #new train needs to be dispatched
            destination_block = self.ctc_ui.sub_block_number_combo.currentText()
            self.backend.dispatch_handler(destination_block)
        elif self.ctc_ui.sub_dispatch_overide_existing_radio.isChecked():
            #existing train needs to be rerouted
            pass


    #maintenance page - Change to send data to backend
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
        

class CtcBackEnd():

    #Stations located green line
    G_STATIONS = ("Pioneer", "Edgebrook", "Station", "Whited", "South Bank", "Centrral", "Inglewood", "Overbrook", "Glenbury", "Dormont", 
                "MT Lebanon", "Poplar", "Castle Shannon", "Dormont", "Glenbury", "Overbrook", "Inglewood", "Central")
    
    #Stations located on red line
    #R_STATIONS = ()

    def __init__(self): 
        super().__init__()
        self.route_data = {}

        #Controls active track data
        self.green_line = Track("Green")
        #self.red_line = Track("Red") #No red line implementation yet
        self.active_line = self.green_line

        #Uncomment when ticket signal is ready-----------------------------------------------
        #self.trackModel.track_tickets.connect(self.handle_tickets)'
        
        self.total_tickets = 0
        self.throughput = 0
        self.train_count = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # 10 Hz update

        #self.wall_clock = global_clock.clock

    def update(self):
        ##Main UI clock element, uncomment when global clock is implemented-------------------------------
        #clock_Time = self.global_clock.text()
        #day_night = self.global_clock.am_pm()
        #full_time = clock_time + " " + day_night
        #self.ctc_ui.current_time_label.setText(full_time)
        pass        
        
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
        
        
    #Scheduling Algorithm
    #Suggested Authority
    #Suggested Speed
        pass

    def upload_train_schedule(self):
        #uploads train schedule file | activated by button
        pass

    def update_dispatch_train_table(self):
        #updates table of trains ready to dispatch
        pass

    def update_active_trains_count(self):
        #Updated mainscreen train count
        #reads number of rows from train data file + manual sent trains
        pass

    def update_override(self):
        if self.ctc_ui.sub_enter_speed_override.value() > 0:
            self.update_override_speed()

        if self.ctc_ui.sub_enter_authority_override.value() > 0:
            self.update_override_authority()

    def update_override_speed(self):
        #updates override speed | input from user
        override_speed = self.ctc_ui.sub_enter_speed_override.text()
        self.test_bench.print_suggested_speed(override_speed)
    
    def update_override_authority(self):
        #updates override authority | input from user
        override_authority = self.ctc_ui.sub_enter_authority_override.text()
        self.test_bench.print_suggested_authority(override_authority)

    def dispatch_handler(self, destination_block):
        #Train dispatch handler | controlls Manually dispatched trains 
        Track.add_active_train(self.train_count, destination_block, "manual")
        self.train_count += 1

    def handle_tickets(self, num_tickets):
        #Takes tickets sold from track model and updates throughput
        self.total_tickets += num_tickets
        self.throughput = self.total_tickets / self.time_elapsed
        #Send throughput to UI
        self.frontend.update_throughput(self.throughput)


    def send_dispatch_train(self):
        
        
        #ctc_dispatch.emit()
        pass
        

    def send_maintenance():
        #ctc_maintenance.emit(block_id, maintenance_val)
        pass

    def send_suggestions():
        #ctc_suggested.emit(speedList, authList)
        pass

    def send_exit_blocks():
        #ctc_exit_blocks.emit()
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
        #elif name == "Red":
        #    self.file_name = Track.RED_LINE
        #ADD ELSE FOR ERROR DETECTION

        self.initialize_blocks()



    def initialize_blocks(self):
        
        file_data = pd.read_excel(self.file_name)
        for index, row in file_data.iterrows():
            block_section = row['Section']
            block_id = int(row['Block Number'])
            block_length = int(row['Block Length (m)'])
            block_speed_limit = int(row['Speed Limit (Km/Hr)'])
            block_station = row['Station'] if isinstance(row['Station'], str) else " "
            block_switch = row['Switch'][7:] if isinstance(row['Switch'], str) else " " #remove "Switch " from string
            block_crossing = 1 if pd.notna(row['Crossing']) else 0
            block_traffic_light = 1 if pd.notna(row['Light']) else 0
            block_transponder = 1 if pd.notna(row['Transponder']) else 0
            block_underground = 1 if pd.notna(row['Underground']) else 0

            #set default values for crossing and light
            crossing_active = 0 #0 open, 1 closed
            light_color = 0 #0 green, 1 red
            occupancy = 0 #0 unoccupied, 1 occupied, 2 failure | TO CHANGE
            switch_state = 0 #0 left, 1 right

            self.blocks[block_id] = {
                'section': block_section,
                'block_id': block_id,
                'occupancy': occupancy,
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



    def set_block_data(self, block_data):
        pass

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