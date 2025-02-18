'''
Author: Aaron Kuchta
Date: 2-17-2025
Revision: 1.1
'''


import sys
import os
import time
import pandas as pd
import openpyxl
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

from centralized_traffic_controller_ui import Ui_MainWindow as CtcUI
#from centralized_traffic_controller_test_bench_ui import CtcTestBench as CtcTestBenchUI


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
    file_data = pd.read_excel(file_name)
    return file_data

#Need to extract 1st row for col headers
#needs updated so only desired vals are shown
def read_map_file(self, map_data):
    if not map_data.empty:
        self.ctc_ui.main_map_table.setColumnCount(len(map_data.columns))
        self.ctc_ui.main_map_table.setRowCount(len(map_data))
        for i in range(len(map_data)):
            for j in range(len(map_data.columns)):
                item = QTableWidgetItem(str(map_data.iat[i, j]))
                self.ctc_ui.main_map_table.setItem(i, j, item)

def read_train_data_file():
    return{

    }

def read_wayside_data():
    return{

    }



# Centralized Traffic Control App

class CentralizedTrafficControlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ctc_ui = CtcUI()
        self.ctc_ui.setupUi(self)

        #CALL TESTBENCH?

        #Variables initialization
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




        # Mode Sliders
        self.ctc_ui.main_mode_slider.sliderReleased.connect(self.toggle_mode)
        #self.ctc_ui.main_line_slider.sliderReleased.connect(self.toggle_active_line)


    #Main Page Widget Functions
    def get_train_schedule(self):
        #open file dialog
        #self.train_schedule = open_file_dialog(self)
        pass
            


    def get_map_data(self):
        self.map_data = open_file_dialog(self)
        read_map_file(self, self.map_data)


    def update_active_trains_count(self):
        #Updated mainscreen train count
        #reads number of rows from train data file + manual sent trains
        pass

    # Navigation buttons for stackked widget
    def switch_to_dispatch_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(1)

    def switch_to_select_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(2)

    def switch_to_maintenance_page(self):
        self.ctc_ui.multiPageWidget.setCurrentIndex(3)

    def on_map_row_clicked(self, row):
        #update block data
        pass

    def update_block_data(self):
        #update block id, length, speed limit | on main page as well as maintenance page
        #self.ctc_ui.main_active_block_id.setText(self.current_block_id)
        #self.ctc_ui.sub_active_block_id.setText(self.current_block_id)
        #self.ctc_ui.main_active_block_length.setText(self.current_block_length)
        #self.ctc_ui.main_active_block_speed_limit.setText(self.current_block_speed_limit)
        pass

    # Activated by mode slider
    def toggle_mode(self):
        if self.ctc_ui.main_mode_slider.value() == 0:
            self.current_mode = "Automatic"
        else:
            self.current_mode = "Maintenance"

        self.update_mode()

    def update_mode(self):
        if self.current_mode == "Automatic":
            self.ctc_ui.main_switch_knob.setEnabled(False)
            self.ctc_ui.sub_activate_maintenance_button.setEnabled(False)
            self.ctc_ui.sub_end_maintenance_button.setEnabled(False)
            self.ctc_ui.main_switch_knob.setSliderPosition(1)

        else:
            self.ctc_ui.main_switch_knob.setEnabled(True)
            self.ctc_ui.sub_activate_maintenance_button.setEnabled(True)
            self.ctc_ui.sub_end_maintenance_button.setEnabled(True)


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

    def update_override_speed(self):
        #updates override speed | input from user
        #self.override_speed = self.ctc_ui.sub_enter_speed_override.text()
        pass

    def update_override_authority(self):
        #updates override authority | input from user
        #self.override_authority = self.ctc_ui.sub_enter_authority_override.text()
        pass

    def send_override_speed_authority(self):
        #sends override speed and authority to selected train | activated by button
        pass

    #maintenance page
    def start_maintenance(self):
        #starts maintenance on selected block | activated by button
        #mark block as maintenance on map
        #send maintenance start command to wayside
        pass

    def end_maintenance(self):
        #ends maintenance on selected block | activated by button 
        #If selected block has no maintenance, button is disabled
        #sends maintenance end command to wayside
        pass

#END UI INTERACTIONS


os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

def main():
    app = QApplication(sys.argv)
    ctc_app = CentralizedTrafficControlApp()
    ctc_app.show()
    #ctc_app.testbench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()