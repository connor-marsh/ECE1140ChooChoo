"""
Train Controller Testbench
"""

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime
from train_controller_testbench_ui import Ui_TestBenchWindow as TrainControllerTestbenchUI

class TrainControllerTestbench(QMainWindow):
    def __init__(self, collection):
        super().__init__()
        self.ui = TrainControllerTestbenchUI()
        self.ui.setupUi(self)

        self.collection = collection
        self.current_train = None

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Set up the button to read inputs and set the values from testbench
        self.ui.tb_input_apply_button.clicked.connect(self.update_train_controller)

    def update_train_controller(self):
        self.current_train = self.collection.train_controller_ui.current_train
        if self.current_train:
            data = {}
            data["actual_speed"] = self.to_float(self.ui.tb_actual_speed_line_edit.text())
            data["speed_limit"] = self.to_float(self.ui.tb_speed_limit_line_edit.text())
            data["wayside_speed"] = self.to_float(self.ui.tb_commanded_wayside_speed_line_edit.text())
            data["wayside_authority"] = self.to_float(self.ui.tb_commanded_wayside_authority_line_edit.text())
            data["emergency_brake"] = self.ui.tb_passenger_emergency_stop_checkbox.isChecked()
            data["beacon_data"] = self.ui.tb_beacon_data_line_edit.text()
            data["actual_temperature"] = self.to_float(self.ui.tb_temperature_status_line_edit.text(), 25.0)
            data["signal_failure"] = self.ui.tb_signal_failure_checkbox.isChecked()
            data["brake_failure"] = self.ui.tb_brake_failure_checkbox.isChecked()
            data["engine_failure"] = self.ui.tb_engine_failure_checkbox.isChecked()
            data["next_station"] = self.ui.tb_next_station_line_edit.text()
            data["announcement"] = self.ui.tb_announcement_checkbox.isChecked()
            self.current_train.set_input_data(testbench_data=data)

    def update(self):
        self.current_train = self.collection.train_controller_ui.current_train
        if (self.current_train):
            self.display_air_conditioning()
            self.display_heating()
            self.display_headlights()
            self.display_internal_lights()
            self.display_doors()
            self.display_emergency_brakes()
            self.display_service_brakes()
            self.display_announcement()

    def display_announcement(self):
        if (self.current_train.announcement):
            self.ui.tb_annunciation_system_display.setText(self.current_train.next_station)

    def display_service_brakes(self):
        if (self.current_train.service_brake):
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_emergency_brakes(self):
        if (self.current_train.emergency_brake):
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_headlights(self):
        if (self.current_train.headlights):
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_internal_lights(self):
        if (self.current_train.interior_lights):
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_air_conditioning(self):
        if (self.current_train.air_conditioning_signal):
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_heating(self):
        if (self.current_train.heating_signal):
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_doors(self):
        if (self.current_train.door_right):
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

        if (self.current_train.door_left):
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def to_float(self, val_str, default=0.0):
        # Helper for string->float conversion
        try:
            return float(val_str)
        except ValueError:
            return default