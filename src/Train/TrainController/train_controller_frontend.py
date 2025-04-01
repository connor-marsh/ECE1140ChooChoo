"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime

from Train.TrainController.train_controller_ui import Ui_MainWindow as TrainControllerUI
from Train.TrainController.train_controller_testbench import TrainControllerTestbench

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class TrainControllerFrontend(QMainWindow):
    def __init__(self, collection, train_integrated=True):
        super().__init__()
        self.train_integrated = train_integrated

        self.collection = collection
        self.current_train = None

        self.ui = TrainControllerUI()
        self.ui.setupUi(self)

        # Defaults for the UI
        self.ui.cabin_temperature_spin_box.setValue(77)

        # Set up buttons to read inputs from UI
        self.ui.control_constants_apply_button.clicked.connect(self.set_k_constants)
        self.ui.headlights_on_button.clicked.connect(self.activate_headlights)
        self.ui.headlights_off_button.clicked.connect(self.deactivate_headlights)
        self.ui.interior_lights_on_button.clicked.connect(self.activate_interior_lights)
        self.ui.interior_lights_off_button.clicked.connect(self.deactivate_interior_lights)
        self.ui.target_speed_apply_button.clicked.connect(self.set_driver_target_speed)

        # Set up the door and emergency buttons to be toggles
        self.ui.door_right_button.setCheckable(True)
        self.ui.door_left_button.setCheckable(True)
        self.ui.emergency_button.setCheckable(True)
        self.ui.door_right_button.toggled.connect(self.handle_right_door)
        self.ui.door_left_button.toggled.connect(self.handle_left_door)
        self.ui.emergency_button.toggled.connect(self.handle_emergency_button)
        self.ui.service_brake_apply_button.clicked.connect(self.handle_service_brake)

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):

        # Set the display values
        if not self.current_train:
            return
        self.current_train = self.collection.train_list[int(self.ui.train_id_dropdown.currentText())-1]
        if self.train_integrated:
            self.current_train = self.current_train.controller

        # Update the clock LCD and the AM/PM label
        self.ui.global_clock_lcd.display(self.current_train.global_clock.text)
        self.ui.am_pm_label.setText(self.current_train.global_clock.am_pm)

        self.display_actual_speed(str(round(self.current_train.actual_speed, 8)))
        self.display_speed_limit(str(round(self.current_train.speed_limit, 8)))
        self.display_authority(str(self.current_train.wayside_authority))
        self.display_cabin_temperature(str(int(round(self.current_train.actual_temperature, 2))))
        self.display_commanded_power(self.current_train.commanded_power)

        # Check if auto or manual mode
        if (self.ui.control_mode_switch.value() == 0):
            # Auto Mode
            self.disable_for_auto()
            self.current_train.manual_mode = False
        else:
            # Manual Mode
            self.enable_for_manual()
            self.current_train.manual_mode = True

        # Update service brake
        if (self.current_train.service_brake):
            self.activate_service_brake()
        else:
            self.deactivate_service_brake()
        
        # Set Failure Lights and handle emergency brakes
        self.activate_signal_failure() if self.current_train.signal_failure else self.deactivate_signal_failure()
        self.activate_brake_failure() if self.current_train.brake_failure else self.deactivate_brake_failure()
        self.activate_engine_failure() if self.current_train.engine_failure else self.deactivate_engine_failure()
        if self.current_train.emergency_brake:
            self.activate_emergency_brake()

        # Set the Input temperature
        self.current_train.desired_temperature = self.ui.cabin_temperature_spin_box.value()

        if (self.current_train.actual_speed > 0):
            self.ui.door_left_button.setEnabled(False)
            self.ui.door_right_button.setEnabled(False)

        # Set next station and on air light
        self.display_next_station()

    def update_train_dropdown(self):
        if self.collection:
            self.ui.train_id_dropdown.clear()  # Clear existing items
            self.ui.train_id_dropdown.addItems([str(i+1) for i in range(len(self.collection.train_list))])  # Add updated list
            if self.current_train==None:
                self.current_train=self.collection.train_list[0]
                
    def display_next_station(self):
        self.ui.next_station_label.setText(self.current_train.next_station)

    def activate_service_brake(self):
        self.ui.service_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")

    def deactivate_service_brake(self):
        self.ui.service_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def set_driver_target_speed(self):
        self.current_train.driver_target_speed = self.ui.target_speed_spin_box.value() # TODO: needs to be converted to m/s
        self.ui.target_speed_lcd.display(self.current_train.driver_target_speed)

    def display_commanded_power(self, power):
        self.ui.commanded_power_lcd.display(power)

    def display_cabin_temperature(self, temperature):
        self.ui.cabin_temperature_lcd.display(temperature)

    def display_authority(self, authority):
        self.ui.authority_lcd.display(authority)

    def display_speed_limit(self, speed_limit):
        self.ui.speed_limit_lcd.display(speed_limit)

    def display_actual_speed(self, speed):
        self.ui.actual_speed_lcd.display(speed)

    def disable_for_auto(self):
        self.ui.target_speed_apply_button.setEnabled(False)
        self.ui.interior_lights_on_button.setEnabled(False)
        self.ui.interior_lights_off_button.setEnabled(False)
        self.ui.headlights_on_button.setEnabled(False)
        self.ui.headlights_off_button.setEnabled(False)
        self.ui.service_brake_apply_button.setEnabled(False)

    def enable_for_manual(self):
        self.ui.target_speed_apply_button.setEnabled(True)
        self.ui.door_left_button.setEnabled(True)
        self.ui.door_right_button.setEnabled(True)
        self.ui.interior_lights_on_button.setEnabled(True)
        self.ui.interior_lights_off_button.setEnabled(True)
        self.ui.headlights_on_button.setEnabled(True)
        self.ui.headlights_off_button.setEnabled(True)
        self.ui.service_brake_apply_button.setEnabled(True)

    def handle_emergency_button(self, checked):
        self.current_train.emergency_brake = checked
        if not checked:
            self.deactivate_emergency_brake()
    
    def activate_emergency_brake(self):
        self.ui.emergency_button.setChecked(True)
        
    def deactivate_emergency_brake(self):
        self.ui.emergency_button.setChecked(False)

    def handle_right_door(self, checked):
        if checked:
            self.current_train.door_right = True
        else:
            self.current_train.door_right = False

    def handle_left_door(self, checked):
        if checked:
            self.current_train.door_left = True
        else:
            self.current_train.door_left = False

    def handle_service_brake(self):
        self.current_train.service_brake = not self.current_train.service_brake

    def activate_headlights(self):
        self.current_train.headlights = True

    def deactivate_headlights(self):
        self.current_train.headlights = False

    def activate_interior_lights(self):
        self.current_train.interior_lights = True

    def deactivate_interior_lights(self):
        self.current_train.interior_lights = False

    def set_k_constants(self):
        self.Kp = self.to_float(self.ui.kp_line_edit.text(), 1.0)
        self.Ki = self.to_float(self.ui.ki_line_edit.text(), 1.0)
        self.ui.control_constants_apply_button.setEnabled(False)
        self.ui.kp_line_edit.setEnabled(False)
        self.ui.ki_line_edit.setEnabled(False)

    def activate_signal_failure(self):
        self.ui.signal_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")

    def deactivate_signal_failure(self):
        self.ui.signal_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")

    def activate_brake_failure(self):
        self.ui.brake_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")
    
    def deactivate_brake_failure(self):
        self.ui.brake_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")

    def activate_engine_failure(self):
        self.ui.engine_failure_light.setStyleSheet("background-color: red; font-weight: bold; font-size: 16px;")

    def deactivate_engine_failure(self):
        self.ui.engine_failure_light.setStyleSheet("background-color: rgb(255, 170, 170); font-weight: bold; font-size: 16px;")
    
    def to_float(self, val_str, default=0.0):
        # Helper for string->float conversion
        try:
            return float(val_str)
        except ValueError:
            return default

def main():
    app = QApplication(sys.argv)
    from train_collection import TrainCollection
    
    train_controller_frontend = TrainControllerFrontend(None)
    collection = TrainCollection(num_trains=3, controller=train_controller_frontend)
    train_controller_frontend.collection = collection
    train_controller_frontend.update_train_dropdown()
    train_controller_frontend.current_train = collection.train_list[0]
    train_controller_frontend.show()

    train_controller_testbench = TrainControllerTestbench(collection)
    train_controller_testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()