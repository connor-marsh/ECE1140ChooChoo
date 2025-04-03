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
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QColor

from CTC.centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
#from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
import globals.global_clock as global_clock

class CtcFrontEnd(QMainWindow):
    def __init__(self, backend):
        super().__init__()
        self.ctc_ui = CtcUI()
        self.ctc_ui.setupUi(self)
        self.backend = backend #Establishes backrend refrence

        #Variable initializations
        self.active_block_id = ""
        self.active_block_length = ""
        self.active_block_speed = ""

        self.selected_row = None

        # Connect buttons
        self.ctc_ui.main_switch_to_dispatch_button.clicked.connect(self.switch_to_dispatch_page)
        self.ctc_ui.main_switch_to_select_button.clicked.connect(self.switch_to_select_page)
        self.ctc_ui.main_switch_to_maintenance_button.clicked.connect(self.switch_to_maintenance_page)
        self.ctc_ui.sub_return_button.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button2.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_button3.clicked.connect(self.switch_to_home)
        self.ctc_ui.multiPageWidget.setCurrentIndex(0)# Set Starting page for stacked widget


        self.ctc_ui.main_switch_to_upload_button.clicked.connect(self.get_train_schedule)
        #self.ctc_ui.main_upload_map_button.clicked.connect(self.get_map_data) # Now unused? Double check

        self.ctc_ui.maintenance_toggle.clicked.connect(self.toggle_maintenance_mode)
        self.ctc_ui.main_map_table.cellClicked.connect(self.on_map_row_clicked)
        #self.ctc_ui.main_line_slider.sliderReleased.connect(self.toggle_active_line) #Not implemented yet
        self.ctc_ui.main_switch_knob.valueChanged.connect(self.set_switch_state)
        #self.ctc_ui.sub_confirm_override_button.clicked.connect(self.update_suggested)
        self.ctc_ui.sub_activate_maintenance_button.clicked.connect(self.start_maintenance)
        self.ctc_ui.sub_end_maintenance_button.clicked.connect(self.end_maintenance)
        self.ctc_ui.sub_dispatch_confirm_button.clicked.connect(self.dispatch_pressed)
        #self.toggle_mode() #toggles manual mode, NEEDS CHANGED 

        self.toggle_maintenance_mode()
        self.initialize_map()
        self.initialize_block_combo()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.frontend_update)
        self.timer.start(50)  # 10 Hz update - change to slower update for performance??

        self.wall_clock = global_clock.clock

    def frontend_update(self):
        self.update_clock() #update clock label
        self.update_throughput() #update throughput label
        self.update_map() #update track data table
        self.ctc_ui.active_train_number_label.setText(str(self.backend.train_count))


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
        block_info = self.backend.active_line.blocks[row]
        self.update_block_data_labels(block_info)

    def update_block_data_labels(self, block_info):
        #update block id, length, speed limit | on main page as well as maintenance page
        self.ctc_ui.main_active_block_id.setText(str(block_info.id))
        self.ctc_ui.sub_active_block_id.setText(str(block_info.id))
        self.ctc_ui.main_active_block_length.setText(str(round(block_info.length)))
        self.ctc_ui.main_active_block_speed_limit.setText(str(round(block_info.speed_limit)))

    def update_clock(self):
        #Main UI clock element
        clock_time = self.wall_clock.text
        day_night = self.wall_clock.am_pm
        full_time = clock_time + " " + day_night
        self.ctc_ui.current_time_label.setText(full_time)

    def initialize_block_combo(self): # HARDCODED
        #initialize block combo box with block ids - currently 1-150
        self.ctc_ui.sub_block_number_combo.clear()
        for i in range(1, 151):
            self.ctc_ui.sub_block_number_combo.addItem(str(i))

    #Map Initialization
    def initialize_map(self):
        self.block_data, self.station_names, self.switches, _, _, _ = self.backend.get_map_data()
        # Update map size 
        self.ctc_ui.main_map_table.setRowCount(len(self.block_data))

        for row_index, block_info in enumerate(self.block_data):
            

            # Set Section and Block ID
            self.ctc_ui.main_map_table.setItem(row_index, 0, QTableWidgetItem(str(block_info.id[0])))
            self.ctc_ui.main_map_table.setItem(row_index, 1, QTableWidgetItem(str(row_index+1)))

            # Set Occupancy | All blocks are unoccupied by default
            occupancy_item = QTableWidgetItem()
            occupancy_item.setBackground(QColor("green"))
            self.ctc_ui.main_map_table.setItem(row_index, 2, occupancy_item)

            # Set Station
            station_item = QTableWidgetItem()
            if block_info.has_station:
                station_item = QTableWidgetItem(str(self.station_names[block_info.id].name))
            else:
                station_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 3, station_item) # NEED TO UPDATE TO DISPLAY STATION NAME

            # Set Switch and Position
            if block_info.id in self.switches:
                switch_value = self.switches[block_info.id].positions[0] # May need to update ID check
            else:
                switch_value = " "
            switch_item = QTableWidgetItem(switch_value)
            if switch_value == " ":
                switch_item.setBackground(QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 4, switch_item)

            # Set Traffic Light
            traffic_light_item = QTableWidgetItem("")
            traffic_light_item.setBackground(QColor("green") if block_info.has_light else QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 5, traffic_light_item)

            # Set Crossing
            crossing_item = QTableWidgetItem("")
            crossing_item.setBackground(QColor("green") if block_info.has_crossing else QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 6, crossing_item)

            # Set Maintenance | All blocks are maintenance free by default
            maintenance_item = QTableWidgetItem()
            maintenance_item.setBackground(QColor("white"))
            self.ctc_ui.main_map_table.setItem(row_index, 7, maintenance_item)

            # Set Transponder
            transponder_item = QTableWidgetItem("")
            transponder_item.setBackground(QColor("green") if block_info.has_beacon else QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 8, transponder_item)

            # Set Underground
            underground_item = QTableWidgetItem("")
            underground_item.setBackground(QColor("green") if block_info.underground else QColor("darkGray"))
            self.ctc_ui.main_map_table.setItem(row_index, 9, underground_item)

        self.ctc_ui.main_map_table.resizeColumnsToContents()

    def update_map(self): # Include updated check for block data?? Check effeciency
        # Updates map with new data (Occupancy, Switch Position, Traffic Light, Crossing Status, and Maintenance | called by update function
        block_data, _, switch_data, switch_states, lights, crossings = self.backend.get_map_data()

        switch_index, light_index, crossing_index = 0, 0, 0

        for row_index, block in enumerate(self.backend.active_line.blocks):
            #print("Displaying Block :", block.id)
            # Update Occupancy
            occupancy_item = QTableWidgetItem()
            occupancy_item.setBackground(QColor("red") if block.occupancy else QColor("green"))
            self.ctc_ui.main_map_table.setItem(row_index, 2, occupancy_item)

            if block.has_switch:
                # Update Switch Position
                switch_item = QTableWidgetItem(str(switch_states[switch_index])) #Would like to swap to actual blocks, not just 0, 1
                self.ctc_ui.main_map_table.setItem(row_index, 4, switch_item)
                switch_index += 1

            if block.has_light:
                # Update Traffic Light
                light_item = QTableWidgetItem()
                light_item.setBackground(QColor("green") if lights[light_index] else QColor("red"))
                self.ctc_ui.main_map_table.setItem(row_index, 5, light_item)
                light_index += 1

            if block.has_crossing:
                # Update Crossing Status
                crossing_item = QTableWidgetItem()
                crossing_item.setBackground(QColor("green") if crossings[crossing_index] else QColor("orange"))
                self.ctc_ui.main_map_table.setItem(row_index, 6, crossing_item)
                crossing_index += 1

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
        elif self.ctc_ui.sub_dispatch_overide_active_radio.isChecked():
            #existing train needs to be rerouted | not implemented yet
            print("Reroute Train Not Implemented")
        else:
            print("Select Dispatch Type Please")

    #maintenance page - Change to send data to backend - UPDATE NEEDED, TRACK CLASS CHANGED
    def start_maintenance(self):
        #starts maintenance on selected block | activated by button
        if self.selected_row is not None:
            block_info = self.backend.active_line.blocks[self.selected_row-1]
            block_info.maintenance = 1
            self.update_maintenance(block_info)
            self.backend.send_block_maintenance(self.selected_row-1, 1) #Calls backend to send data to wayside
            #self.test_bench.print_maintenance(block_info['block_id'], 1)
        
    def end_maintenance(self):
        #ends maintenance on selected block | activated by button 
        if self.selected_row is not None:
            block_info = self.backend.active_line.blocks[self.selected_row-1]
            block_info.maintenance = 0
            self.update_maintenance(block_info)
            self.backend.send_block_maintenance(self.selected_row-1, 0) #Calls backend to send data to wayside
            #self.test_bench.print_maintenance(block_info['block_id'], 0)
    
    def update_maintenance(self, block_info):
        #updates maintenance mode | called by start/end maintenance functions | table SHOULD map to block id
        case = block_info.maintenance
        if case == 0:
            self.ctc_ui.main_map_table.item(self.selected_row-1, 7).setBackground(QColor("white"))
        elif case == 1:
            self.ctc_ui.main_map_table.item(self.selected_row-1, 7).setBackground(QColor("red"))
    
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
        if self.selected_row is not None and self.ctc_ui.maintenance_toggle.isChecked(): # and block has switch
            #set block switch value
            
            knob_state = self.ctc_ui.main_switch_knob.value()
            if knob_state != 1:
                if knob_state == 0:
                    switch_state = 0
                elif knob_state == 2:
                    switch_state = 1
                block_id = self.selected_row-1 #Need to implement block id 
                self.backend.send_switch_states(block_id, switch_state)

