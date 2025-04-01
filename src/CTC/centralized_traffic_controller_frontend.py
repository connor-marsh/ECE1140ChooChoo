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

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
from centralized_traffic_controller_backend import CtcBackend
from centralized_traffic_controller_test_bench_ui import Ui_ctc_TestBench as CtcTestBenchUI
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
            block_id = 0 #Need to implement block id 
            self.backend.send_switch_states(block_id, switch_state)

