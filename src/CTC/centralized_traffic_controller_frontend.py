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
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QButtonGroup
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

        self.ctc_ui.maintenance_toggle.clicked.connect(self.toggle_maintenance_mode)
        self.ctc_ui.main_map_table.cellClicked.connect(self.on_map_row_clicked)
        self.ctc_ui.sub_dispatch_train_table.cellClicked.connect(self.on_dispatch_row_clicked)
        self.ctc_ui.sub_dispatch_station_select_radio.toggled.connect(self.destination_radio_selected)
        self.ctc_ui.sub_dispatch_block_select_radio.toggled.connect(self.destination_radio_selected)
        self.ctc_ui.main_line_slider.valueChanged.connect(self.toggle_active_line)
        self.ctc_ui.main_switch_knob.valueChanged.connect(self.set_switch_state)
        self.ctc_ui.sub_confirm_override_button.clicked.connect(self.update_suggested_values)
        self.ctc_ui.sub_activate_maintenance_button.clicked.connect(self.start_maintenance)
        self.ctc_ui.sub_end_maintenance_button.clicked.connect(self.end_maintenance)
        self.ctc_ui.sub_dispatch_confirm_button.clicked.connect(self.dispatch_pressed)
        self.ctc_ui.sub_active_trains_table.cellClicked.connect(self.update_train_mode_radio)
        self.ctc_ui.sub_select_manual_radio.clicked.connect(self.toggle_train_mode)

        self.destination_radio_group = QButtonGroup(self)
        self.destination_radio_group.addButton(self.ctc_ui.sub_dispatch_station_select_radio)
        self.destination_radio_group.addButton(self.ctc_ui.sub_dispatch_block_select_radio)
        self.destination_radio_group.setExclusive(True) 

        self.toggle_maintenance_mode()
        self.initialize_map()
        self.initialize_block_combo()
        self.initialize_station_combo()
        self.initialize_train_schedule()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.frontend_update)
        self.timer.start(50)  # 10 Hz update - change to slower update for performance??

        self.wall_clock = global_clock.clock

        self.known_train_count = 0

    def frontend_update(self):
        self.update_clock() #update clock label
        self.update_throughput() #update throughput label
        self.update_map() #update track data table
        self.ctc_ui.active_train_number_label.setText(str(self.backend.active_line.active_trains_count))
        self.update_active_train_table() #Needs updated to work with new backend
        self.update_dispatch_button()
        self.update_train_select_combo()

    def toggle_active_line(self):
        if self.ctc_ui.main_line_slider.value() == 0:
            self.backend.active_line = self.backend.lines["Green"]
            print("Active Line: ", self.backend.active_line.name)
            self.initialize_map()
            self.initialize_block_combo()
            self.initialize_station_combo()
        elif self.ctc_ui.main_line_slider.value() == 1:
            self.backend.active_line = self.backend.lines["Red"]
            print("Active Line: ", self.backend.active_line.name)
            self.initialize_map()
            self.initialize_block_combo()
            self.initialize_station_combo()

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
            
        file_data = pd.read_excel(file_name, header=None)
        return file_data
    
    def initialize_train_schedule(self):
        file_name = "src/CTC/Green_Line_Schedule.xlsx"
        route_schedules = pd.read_excel(file_name, header=None)
        self.backend.process_route_data(route_schedules)
        self.update_route_table()

    def get_train_schedule(self):
        #open file dialog
        route_schedules = self.open_file_dialog()
        self.backend.process_route_data(route_schedules)
        self.update_route_table()

    def update_route_table(self):
        self.ctc_ui.sub_dispatch_train_table.setRowCount(len(self.backend.active_line.routes))
        max_stations = max(len(stations) for stations in self.backend.active_line.routes.values())

        # Set the number of columns: 1 for ID, 1 for Route Name, then columns for each station
        self.ctc_ui.sub_dispatch_train_table.setColumnCount(max_stations + 2)
        self.ctc_ui.sub_dispatch_train_table.setHorizontalHeaderLabels(['ID', 'Route Name'] + [f'Station {i+1}' for i in range(max_stations)])

        for row_idx, (route_name, stations) in enumerate(self.backend.active_line.routes.items()):
            # Add ID column (using row_idx to generate a unique ID for each route)
            self.ctc_ui.sub_dispatch_train_table.setItem(row_idx, 0, QTableWidgetItem(str(row_idx + 1)))  # IDs start from 1

            # Add Route Name column
            self.ctc_ui.sub_dispatch_train_table.setItem(row_idx, 1, QTableWidgetItem(route_name))

            # Add Stations columns
            for col_idx, station in enumerate(stations):
                self.ctc_ui.sub_dispatch_train_table.setItem(row_idx, col_idx + 2, QTableWidgetItem(station))

            # Fill remaining columns with empty text if route has fewer stations than the max
            for col_idx in range(len(stations) + 2, self.ctc_ui.sub_dispatch_train_table.columnCount()):
                self.ctc_ui.sub_dispatch_train_table.setItem(row_idx, col_idx, QTableWidgetItem(''))

    def on_map_row_clicked(self, row, column):
        #stores data for clicked block
        self.selected_row = row+1 #Stores for later use
        block_info = self.backend.active_line.blocks[row]
        self.update_block_data_labels(block_info)

    def on_dispatch_row_clicked(self, row, column):
        #break exclusivity to allow unchecking
        self.destination_radio_group.setExclusive(False)

        if self.ctc_ui.sub_dispatch_station_select_radio.isChecked():
            self.ctc_ui.sub_dispatch_station_select_radio.setChecked(False)
        elif self.ctc_ui.sub_dispatch_block_select_radio.isChecked():
            self.ctc_ui.sub_dispatch_block_select_radio.setChecked(False)

        #Restore exclusivity
        self.destination_radio_group.setExclusive(True)
        
        

    def destination_radio_selected(self):
        destination_radio_selected = self.ctc_ui.sub_dispatch_station_select_radio.isChecked() or self.ctc_ui.sub_dispatch_block_select_radio.isChecked()
        if destination_radio_selected:
            self.ctc_ui.sub_dispatch_train_table.clearSelection()

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

    def initialize_block_combo(self): 
        if self.backend.active_line.name == "Green":
            #initialize block combo box with block ids - Green 1-150
            self.ctc_ui.sub_block_number_combo.clear()
            for i in range(1, 153):
                self.ctc_ui.sub_block_number_combo.addItem(str(i))
        elif self.backend.active_line.name == "Red":
            #initialize block combo box with block ids - Red 1-76
            self.ctc_ui.sub_block_number_combo.clear()
            for i in range(1, 78):
                self.ctc_ui.sub_block_number_combo.addItem(str(i))
        else:
            QTimer.singleShot(100, self.initialize_block_combo) # If neither track active, retry in 100ms

    def initialize_station_combo(self):
        #initialize station combo box with station names
        self.ctc_ui.sub_station_combo.clear()
        for station in self.backend.active_line.STATIONS_BLOCKS.keys():
            self.ctc_ui.sub_station_combo.addItem(station)

    def update_train_select_combo(self):
        #initialize train combo box with active trains
        if self.known_train_count != self.backend.active_line.active_trains_count:
            self.known_train_count = self.backend.active_line.active_trains_count
            self.ctc_ui.sub_select_active_train_combo.clear()
            for train in self.backend.active_line.current_trains:
                train_id = str(train.train_id)
                self.ctc_ui.sub_select_active_train_combo.addItem(train_id)


    def fill_active_trains_table(self, table_widget, active_trains, blocks):
        table_widget.setRowCount(len(active_trains)) 

        for row, train in enumerate(active_trains):
            train_id = str(train.train_id)
            current_block = str(train.current_block)
            remaining_stops = str(len(train.route) - train.route_index)
            if int(remaining_stops) > 0:
                upcoming_stop = str(blocks[train.route[train.route_index] - 1].id)
            else:
                upcoming_stop = "None"

            current_mode = str(train.mode)

            items = [
                QTableWidgetItem(train_id),
                QTableWidgetItem(current_block),
                QTableWidgetItem(upcoming_stop),
                QTableWidgetItem(remaining_stops),
                QTableWidgetItem(current_mode),
            ]

            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignCenter)
                table_widget.setItem(row, col, item)

    def update_active_train_table(self):
        active_trains = self.backend.active_line.current_trains
        blocks = self.backend.active_line.blocks

        self.fill_active_trains_table(self.ctc_ui.main_active_trains_table, active_trains, blocks)
        self.fill_active_trains_table(self.ctc_ui.sub_active_trains_table, active_trains, blocks)            

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
                switch_value = str(self.switches[block_info.id].positions[0])
                # print("Block id:", block_info.id, "value:", switch_value)  # Debugging output
            else:
                switch_value = " "  # Default value

            switch_item = QTableWidgetItem()
            switch_item.setText(switch_value) 

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
        self.block_data, self.station_names, self.switches, switch_state, lights, crossings = self.backend.get_map_data()

        switch_index, light_index, crossing_index = 0, 0, 0

        for row_index, block in enumerate(self.backend.active_line.blocks):
            #print("Displaying Block :", block.id)
            # Update Occupancy
            occupancy_item = QTableWidgetItem()
            occupancy_item.setBackground(QColor("red") if block.occupancy else QColor("green"))
            self.ctc_ui.main_map_table.setItem(row_index, 2, occupancy_item)
            
            if block.has_switch:
                # Update Switch Position
                # print("Block ID: ", block.id, "Switch val", block.switch_state)
                if block.switch_state == 0:
                    switch_value = str(self.switches[block.id].positions[0]) 
                elif block.switch_state == 1:
                    switch_value = str(self.switches[block.id].positions[1]) 
                switch_item = QTableWidgetItem()
                switch_item.setText(switch_value) 

                self.ctc_ui.main_map_table.setItem(row_index, 4, switch_item)

            if block.has_light:
                # Update Traffic Light
                light_item = QTableWidgetItem()
                light_item.setBackground(QColor("green") if  not block.light_state else QColor("red"))
                self.ctc_ui.main_map_table.setItem(row_index, 5, light_item)
                light_index += 1

            if block.has_crossing:
                # Update Crossing Status
                crossing_item = QTableWidgetItem()
                crossing_item.setBackground(QColor("green") if not block.crossing_state else QColor("orange"))
                self.ctc_ui.main_map_table.setItem(row_index, 6, crossing_item)
                crossing_index += 1
    
    def update_train_mode_radio(self):
        selected_item = self.ctc_ui.sub_active_trains_table.selectedItems()
        if selected_item:
            train = self.backend.active_line.current_trains[selected_item[0].row()]
            if train.mode == "manual":
                self.ctc_ui.sub_select_manual_radio.setChecked(True)
            elif train.mode == "auto":
                self.ctc_ui.sub_select_manual_radio.setChecked(False)
            else:
                pass

    def toggle_train_mode(self):
        if self.ctc_ui.sub_select_manual_radio.isChecked():
            selected_item = self.ctc_ui.sub_active_trains_table.selectedItems()
            if selected_item:
                train = self.backend.active_line.current_trains[selected_item[0].row()]
                train.mode = "manual"
                self.update_train_mode_radio()
        else:
            selected_item = self.ctc_ui.sub_active_trains_table.selectedItems()
            if selected_item:
                train = self.backend.active_line.current_trains[selected_item[0].row()]
                train.mode = "automatic"
                self.update_train_mode_radio()

    def update_suggested_values(self):
        selected_items = self.ctc_ui.sub_active_trains_table.selectedItems()
        if selected_items:
            selected_item = selected_items[0]
            # Do something with selected_item
        else:
            selected_item = None

        
        if selected_item is not None:
            trainIndex = selected_item.row()
            suggested_speed = self.ctc_ui.sub_enter_speed_override.value()
            suggested_auth = self.ctc_ui.sub_enter_authority_override.value()
            self.backend.set_suggested_values(trainIndex, suggested_speed, suggested_auth)

            
    def update_throughput(self):
        #updates throughput label on UI
        self.ctc_ui.main_throughput_label.setText(str(round(self.backend.throughput,2)))

    def update_dispatch_button(self):
        # Updates button state based off selected buttons
        train_selected = self.ctc_ui.sub_dispatch_overide_new_radio.isChecked() or self.ctc_ui.sub_dispatch_overide_active_radio.isChecked()
        destination_selected = (self.ctc_ui.sub_dispatch_station_select_radio.isChecked() and self.ctc_ui.sub_station_combo.currentText() != "") or (self.ctc_ui.sub_dispatch_block_select_radio.isChecked() and self.ctc_ui.sub_block_number_combo.currentText() != "") or self.ctc_ui.sub_dispatch_train_table.selectedItems()
        if train_selected and destination_selected:
            self.ctc_ui.sub_dispatch_confirm_button.setEnabled(True)
        else:
            self.ctc_ui.sub_dispatch_confirm_button.setEnabled(False)

    def dispatch_pressed(self):
        # Check if creating new train or rerouting existing train
        if self.ctc_ui.sub_dispatch_overide_new_radio.isChecked():
            createNewTrain = True
            train_num = None
        elif self.ctc_ui.sub_dispatch_overide_active_radio.isChecked():
            #existing train needs to be rerouted | not implemented yet
            createNewTrain = False
            train_num = self.ctc_ui.sub_select_active_train_combo.currentText()
        else:
            print("Select Dispatch Type Please")
            return # We are done here if user didnt select type
        
        # Now check type of dispatch
        if self.ctc_ui.sub_dispatch_station_select_radio.isChecked():
            #dispatch to station
            destination_station = self.ctc_ui.sub_station_combo.currentText() #CHANGED FROM INDEX
            self.backend.dispatch_handler(destination_station, 'station', new_train=createNewTrain, selected_train = train_num)
        elif self.ctc_ui.sub_dispatch_block_select_radio.isChecked():
            #dispatch to block
            destination_block = self.ctc_ui.sub_block_number_combo.currentText()
            self.backend.dispatch_handler(destination_block, 'block', new_train=createNewTrain, selected_train = train_num)
        elif self.ctc_ui.sub_dispatch_train_table.selectedItems():
            #dispatch to selected route
            selected_item = self.ctc_ui.sub_dispatch_train_table.selectedItems()[0]
            row = selected_item.row()
            route_name_item = self.ctc_ui.sub_dispatch_train_table.item(row, 1) 
            
            if route_name_item:
                route_name = route_name_item.text()
                #print("Dispatching to route:", route_name)
                self.backend.dispatch_handler(route_name, 'route', new_train=createNewTrain, selected_train = train_num) 

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
                self.backend.active_line.blocks[self.selected_row-1].switch_state = switch_state
                self.backend.send_switch_states(block_id, switch_state)