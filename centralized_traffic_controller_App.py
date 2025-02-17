'''
Author: Aaron Kuchta
Date: 2021-07-26
Revision: 1.0
'''


import sys
import os
import time
from PyQt5.QtWidgets import QApplication, QMainWindow

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

def read_schedule_file():
    return{

    }

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
        self.ctc_ui.stackedWidget.setCurrentIndex(0)

        # clock timer
        #self.simulated_time = QTime(12, 0, 0)
        #self.clock_timer = QTimer(self)
        #self.clock_timer.timeout.connect(self.update_clock)
        #self.clock_timer.start(1000)



        # Connect buttons
        self.ctc_ui.sub_return.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_2.clicked.connect(self.switch_to_home)
        self.ctc_ui.sub_return_3.clicked.connect(self.switch_to_home)

        self.ctc_ui.main_switch_to_dispatch.clicked.connect(self.switch_to_dispatch_page)
        self.ctc_ui.main_switch_to_select.clicked.connect(self.switch_to_select_page)
        self.ctc_ui.main_switch_to_maintenance.clicked.connect(self.switch_to_maintenance_page)

        # Mode Slider 
        self.ctc_ui.main_mode_slider.sliderReleased.connect(self.toggle_mode)


    def switch_to_home(self):
        self.ctc_ui.stackedWidget.setCurrentIndex(0)

    def switch_to_dispatch_page(self):
        self.ctc_ui.stackedWidget.setCurrentIndex(1)

    def switch_to_select_page(self):
        self.ctc_ui.stackedWidget.setCurrentIndex(2)

    def switch_to_maintenance_page(self):
        self.ctc_ui.stackedWidget.setCurrentIndex(3)

    def toggle_mode(self):
        if self.ctc_ui.main_mode_slider.value() == 0:
            self.current_mode = "Automatic"
        else:
            self.current_mode = "Manual"

        self.update_mode()

    def update_mode(self):
        if self.current_mode == "Automatic":
            self.ctc_ui.main_switch_knob.setEnabled(False)
            self.ctc_ui.start_maintenance_button.setEnabled(False)
            self.ctc_ui.end_maintenance_button.setEnabled(False)
            self.ctc_ui.main_switch_knob.setSliderPosition(1)
        else:
            self.ctc_ui.main_switch_knob.setEnabled(True)
            self.ctc_ui.start_maintenance_button.setEnabled(True)
            self.ctc_ui.end_maintenance_button.setEnabled(True)
            
    





os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

def main():
    app = QApplication(sys.argv)
    ctc_app = CentralizedTrafficControlApp()
    ctc_app.show()
    #ctc_app.testbench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()