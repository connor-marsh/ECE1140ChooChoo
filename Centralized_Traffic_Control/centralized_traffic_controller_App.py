'''
Author: Aaron Kuchta
Date: 2-20-2025
Revision: 1.3
'''


import sys
import os
import time
import pandas as pd
import openpyxl
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI


'''
Front End data reading
'''

def read_ctc_test_bench_data():
    return{

    }

def read_ctc_data():
    return{

    }

def open_file_dialog(self):
    # Opens file dialog
    file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel Files (*.xlsx)')

    if not file_name:
        return None  # If no file is selected, return None
        
    file_data = pd.read_excel(file_name)
    return file_data
    
def read_train_data_file():
    return{

    }

def read_wayside_data():
    return{

    }

# Centralized Traffic Control Test Bench App
class CentralizedTrafficControlTestBenchApp(QMainWindow):
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
            print(f"Block input: {block_states}")
        if crossing_input:
            railway_crossing_states = [int(x) for x in crossing_input.split(",")]
        if light_input:
            light_states = [int(x) for x in light_input.split(",")]
        if switch_input:
            switch_states = [int(x) for x in switch_input.split(",")]

        self.ctc_app.get_test_bench_data(block_states, railway_crossing_states, light_states, switch_states)  

    def print_suggestions(self, speed, auth ):
        self.ctc_tb_ui.tb_out_speed.setText(speed)
        self.ctc_tb_ui.tb_out_speed.setText(auth)
    
    def print_maintenance(self, block_id, maintenance_val):
        message = ("Block " + str(block_id) + ": " + str(maintenance_val))
        self.ctc_tb_ui.tb_out_maintenance.setText(message)

    def print_switch_state(self, block_id, switch_state):
        message = ("Block " + str(block_id) + ": " + str(switch_state))
        self.ctc_tb_ui.tb_out_switch_states.setText(message)

# Centralized Traffic Control App

class CentralizedTrafficControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ctc_ui = CtcUI()
        self.ctc_ui.setupUi(self)

        self.test_bench = CentralizedTrafficControlTestBenchApp(self)

        #Variables initialization

        self.block_data = {}

        self.current_block_section = " "
        self.current_block_id = 0
        self.current_block_occupancy = 0
        self.current_block_speed_limit = 0
        self.current_block_station = " "
        self.current_block_length = 0
        self.current_block_infrastructure = " "
        self.current_block_switch = " "
        self.current_block_railway_crossing = " "
        self.current_block_traffic_light = " "
        self.current_block_mainenance = 0

        self.train_count = 0
        self.current_line = 0
        self.current_mode = "Automatic"

        self.current_block_id = " "
        self.current_block_occupancy = " "
        self.current_block_speed_limit = " "
        self.suggested_authority = 0 #meters
        self.suggested_speed = 0 #m/s

        # Set Starting page for stacked widget
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)

        

        # clock timer
        #self.simulated_time = QTime(12, 0, 0)
        #self.clock_timer = QTimer(self)
        #self.clock_timer.timeout.connect(self.update_clock)
        #self.clock_timer.start(1000)



        # Connect buttons
        self.ctc_ui.main_switch_to_dispatch_button.clicked.connect(self.switch_to_dispatch_page)
        self.ctc_ui.main_switch_to_select_button.clicked.connect(self.switch_to_select_page)
        self.ctc_ui.main_switch_to_maintenance_button.clicked.connect(self.switch_to_maintenance_page)
        self.ctc_ui.main_switch_to_upload_button.clicked.connect(self.get_train_schedule)
        self.ctc_ui.main_upload_map_button.clicked.connect(self.get_map_data)

        self.ctc_ui.sub_return_button.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button2.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button3.clicked.connect(self.switch_to_home)

        self.ctc_ui.maintenance_toggle.clicked.connect(self.toggle_maintenance_mode)

        self.ctc_ui.main_map_table.cellClicked.connect(self.on_map_row_clicked)

        # Mode Sliders
        self.ctc_ui.main_mode_slider.sliderReleased.connect(self.toggle_mode)
        #self.ctc_ui.main_line_slider.sliderReleased.connect(self.toggle_active_line) #Not implemented yet

        self.ctc_ui.sub_confirm_override_button.clicked.connect(self.update_override)

        self.ctc_ui.sub_activate_maintenance_button.clicked.connect(self.start_maintenance)
        self.ctc_ui.sub_end_maintenance_button.clicked.connect(self.end_maintenance)

        self.toggle_mode()
        self.toggle_maintenance_mode()


    def get_test_bench_data(self, block_states, railway_crossing_states, light_states, switch_states):

        #index counts for loop
        cross_i = 0
        light_i = 0
        switch_i = 0
        

        for block_id, block_info in self.block_data.items():

            #ensures only given blocks are updated
            if block_id  <= len(block_states):
                block_info['occupancy'] = block_states[block_id-1]

            if block_info['crossing'] == 1 and cross_i < len(railway_crossing_states):
                block_info['crossing_active'] = railway_crossing_states[cross_i]
                cross_i += 1
            
            if block_info['traffic_light'] == 1 and light_i < len(light_states):
                block_info['light_color'] = light_states[light_i]
                light_i += 1

            if block_info['switch'] != 0 and switch_i < len(switch_states):
                block_info['switch_state'] = switch_states[switch_i]
                switch_i += 1
        
            self.update_map_row(block_info)


    #Main Page Widget Functions
    def get_train_schedule(self):
        #open file dialog
        #self.train_schedule = open_file_dialog(self)
        pass
            

    def open_file_dialog(self):
        # Opens file dialog
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Excel Files (*.xlsx)')

        if not file_name:
            return None  # If no file is selected, return None
        
        file_data = pd.read_excel(file_name)
        return file_data
    
    def read_map_file(self, map_data):
        for index, row in map_data.iterrows():
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
            light_color = 0 #0 green, 1 yellow, 2 red
            occupancy = 0 #0 unoccupied, 1 occupied, 2 failure
            switch_state = 0 #0 left, 1 right

            self.block_data[block_id] = {
                'section': block_section,
                'block_id': block_id,
                'occupancy': occupancy,
                'block_length': block_length,
                'speed_limit': block_speed_limit,
                'station': block_station,
                'switch': block_switch,
                'switch_state': switch_state,
                'crossing': block_crossing,
                'crossing_active': crossing_active,
                'traffic_light': block_traffic_light,
                'light_color': light_color,
                'transponder': block_transponder,
                'underground': block_underground
            }

    def get_map_data(self):
        map_data = open_file_dialog(self)
        if(map_data is not None):
            self.read_map_file(map_data)
            self.initialize_map()

    def initialize_map(self):
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


    def update_map_row(self, block_info):
        #updates data per block
        row_index = block_info['block_id'] - 1

        #print(f"Block #: {block_info['block_id']} Block crossing: {block_info['crossing']}") #Debug

        case = block_info['occupancy']
        if case == 0:
            self.ctc_ui.main_map_table.item(row_index, 2).setBackground(QColor("green"))
        elif case == 1:
            self.ctc_ui.main_map_table.item(row_index, 2).setBackground(QColor("orange"))
        elif case == 2:
            self.ctc_ui.main_map_table.item(row_index, 2).setBackground(QColor("red"))
        
        case = block_info['light_color']
        if block_info['traffic_light'] == 1:
            if case == 0:
                self.ctc_ui.main_map_table.item(row_index, 5).setBackground(QColor("green"))
            elif case == 1:
                self.ctc_ui.main_map_table.item(row_index, 5).setBackground(QColor("yellow"))
            elif case == 2:
                self.ctc_ui.main_map_table.item(row_index, 5).setBackground(QColor("red"))

        
        case = block_info['crossing_active']
        if block_info['crossing'] == 1:
            if case == 0:
                self.ctc_ui.main_map_table.item(row_index, 6).setBackground(QColor("green"))
            elif case == 1:
                self.ctc_ui.main_map_table.item(row_index, 6).setBackground(QColor("red"))

        #NEED TO ADD SECTION FOR SWITCH STATE
        



    def update_maintenance(self, block_info):
        #updates maintenance mode | activated by button
        case = block_info['maintenance']
        if case == 0:
            self.ctc_ui.main_map_table.item(block_info['block_id']-1, 7).setBackground(QColor("white"))
        elif case == 1:
            self.ctc_ui.main_map_table.item(block_info['block_id']-1, 7).setBackground(QColor("red"))
        

    def update_active_trains_count(self):
        #Updated mainscreen train count
        #reads number of rows from train data file + manual sent trains
        pass

    # Navigation buttons for stacked widget
    def switch_to_dispatch_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(1)

    def switch_to_select_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(2)

    def switch_to_maintenance_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(3)

    def on_map_row_clicked(self, row, column):
        #stores data for clicked block
        self.selected_row = row+1 #Stores for later use
        block_info = self.block_data.get(row+1)
        self.update_block_data(block_info)

        

    def update_block_data(self,block_info):
        #update block id, length, speed limit | on main page as well as maintenance page
        self.ctc_ui.main_active_block_id.setText(str(block_info['block_id']))
        self.ctc_ui.sub_active_block_id.setText(str(block_info['block_id']))
        self.ctc_ui.main_active_block_length.setText(str(block_info['block_length']))
        self.ctc_ui.main_active_block_speed_limit.setText(str(block_info['speed_limit']))
        pass

    # Activated by mode slider
    def toggle_mode(self):
        if self.ctc_ui.main_mode_slider.value() == 0:
            self.current_mode = "Automatic"
        else:
            self.current_mode = "Manual"

        self.update_mode()

    def update_mode(self):
        if self.current_mode == "Automatic":
            self.ctc_ui.sub_dispatch_overide_new_radio.setEnabled(False)
            self.ctc_ui.sub_dispatch_overide_active_radio.setEnabled(False)
            self.ctc_ui.sub_select_active_train_combo.setEnabled(False)
            self.ctc_ui.sub_block_letter_combo.setEnabled(False)
            self.ctc_ui.sub_block_number_combo.setEnabled(False)
            self.ctc_ui.sub_dispatch_confirm_button.setEnabled(False)
            self.ctc_ui.sub_enter_authority_override.setEnabled(False)
            self.ctc_ui.sub_enter_speed_override.setEnabled(False)
            self.ctc_ui.sub_confirm_override_button.setEnabled(False)
            #DISABLE AUTO DISPATCH
        else:
            self.ctc_ui.sub_dispatch_overide_new_radio.setEnabled(True)
            self.ctc_ui.sub_dispatch_overide_active_radio.setEnabled(True)
            self.ctc_ui.sub_select_active_train_combo.setEnabled(True)
            self.ctc_ui.sub_block_letter_combo.setEnabled(True)
            self.ctc_ui.sub_block_number_combo.setEnabled(True)
            self.ctc_ui.sub_dispatch_confirm_button.setEnabled(True)
            self.ctc_ui.sub_enter_authority_override.setEnabled(True)
            self.ctc_ui.sub_enter_speed_override.setEnabled(True)
            self.ctc_ui.sub_confirm_override_button.setEnabled(True)

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
    #Sub Page Widget Functions

    #dispatch page
    def switch_to_home(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)

    def upload_train_schedule(self):
        #uploads train schedule file | activated by button
        pass

    def update_dispatch_train_table(self):
        #updates table of trains ready to dispatch
        pass

    def update_train_to_dispatch(self):
        #updates train that is ready dispatch | Selected from table or manual input, mutally exclusive
        pass

    def dispatch_train(self):
        #dispatches selected train | activated by button | disabled if no train selected
        pass

    #select train page
    def update_active_train_table(self):
        #updates table of active trains on track
        pass

    def update_current_train_values(self):
        #updates current train values | selected from table
        pass

    def update_override(self):

        if self.ctc_ui.sub_enter_speed_override.value() > 0:
            self.update_override_speed()
        if self.ctc_ui.sub_enter_authority_override.value() > 0:
            self.update_override_authority()

    def update_override_speed(self):
        #updates override speed | input from user
        self.override_speed = self.ctc_ui.sub_enter_speed_override.text()
        #send to test bench

    def update_override_authority(self):
        #updates override authority | input from user
        self.override_authority = self.ctc_ui.sub_enter_authority_override.text()
        #send to test bench

    #maintenance page
    def start_maintenance(self):
        #starts maintenance on selected block | activated by button
        if self.selected_row is not None:
            block_info = self.block_data.get(self.selected_row)
            block_info['maintenance'] = 1
            self.update_maintenance(block_info)
            self.test_bench.print_maintenance(block_info['block_id'], 1)
        

    def end_maintenance(self):
        #ends maintenance on selected block | activated by button 
        if self.selected_row is not None:
            block_info = self.block_data.get(self.selected_row)
            block_info['maintenance'] = 0
            self.update_maintenance(block_info)
            self.test_bench.print_maintenance(block_info['block_id'], 0)
        

#END UI INTERACTIONS


os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

def main():
    app = QApplication(sys.argv)
    ctc_app = CentralizedTrafficControlApp()

    ctc_app.show()
    ctc_app.test_bench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()