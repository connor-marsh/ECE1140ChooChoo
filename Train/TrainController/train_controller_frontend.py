"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""
import sys
import os

# Add the parent directory (if needed)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime

from train_controller_ui import Ui_MainWindow as TrainControllerUI
from train_controller_testbench_ui import Ui_TestBenchWindow as TrainControllerTestbenchUI

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class TrainControllerFrontend(QMainWindow):
    def __init__(self, collection):
        super().__init__()

        self.collection = collection
        self.current_train = None

        self.ui = TrainControllerUI()
        self.ui.setupUi(self)
        # Defaults for the UI
        self.ui.cabin_temperature_spin_box.setValue(int(temp_conversion(self.desired_temperature)))

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

        # Set up the button to read inputs and set the values from testbench
        self.testbench.ui.tb_input_apply_button.clicked.connect(self.read_testbench_inputs)

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Set up timer for updating the clock every second
        self.simulated_time = QTime(6, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

    def update(self):
        # Set the display values
        self.display_actual_speed(str(self.current_train.actual_speed))
        self.display_speed_limit(str(self.current_train.speed_limit))
        self.display_authority(str(self.current_train.commanded_authority))
        self.display_cabin_temperature(str(self.current_train.temperature_status))
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
        if self.passenger_emergency_stop:
            self.activate_emergency_brake()

        # Set the Input temperature
        self.current_train.desired_temperature = self.ui.cabin_temperature_spin_box.value()

        if (self.current_train.actual_speed > 0):
            self.ui.door_left_button.setEnabled(False)
            self.ui.door_right_button.setEnabled(False)

        # Set next station and on air light
        self.display_next_station()
        self.activate_announcement_light() if self.current_train.announcement else self.deactivate_announcement_light()

    def activate_announcement_light(self):
        self.ui.announcement_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def deactivate_announcement_light(self):
        self.ui.announcement_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")

    def display_next_station(self):
        self.ui.next_station_label.setText(self.next_station)

    def activate_service_brake(self):
        self.ui.service_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")

    def deactivate_service_brake(self):
        self.ui.service_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        self.ui.service_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def set_driver_target_speed(self):
        self.driver_target_speed = speed_conversion_in(self.ui.target_speed_spin_box.value()) # TODO: needs to be converted to m/s
        self.ui.target_speed_lcd.display(speed_conversion(self.driver_target_speed))

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

    def enable_for_manual(self):
        self.ui.target_speed_apply_button.setEnabled(True)
        self.ui.door_left_button.setEnabled(True)
        self.ui.door_right_button.setEnabled(True)
        self.ui.interior_lights_on_button.setEnabled(True)
        self.ui.interior_lights_off_button.setEnabled(True)
        self.ui.headlights_on_button.setEnabled(True)
        self.ui.headlights_off_button.setEnabled(True)

    def handle_emergency_button(self, checked):
        if checked:
            self.emergency_brake = True
        else:
            self.emergency_brake = False
            self.passenger_emergency_stop = False
    
    def activate_emergency_brake(self):
        self.ui.emergency_button.setChecked(True)

    def handle_right_door(self, checked):
        if checked:
            self.door_right = True
        else:
            self.door_right = False

    def handle_left_door(self, checked):
        if checked:
            self.door_left = True
        else:
            self.door_left = False

    def activate_headlights(self):
        self.headlights = True

    def deactivate_headlights(self):
        self.headlights = False

    def activate_interior_lights(self):
        self.interior_lights = True

    def deactivate_interior_lights(self):
        self.interior_lights = False

    def activate_heating(self):
        self.heating_signal = True

    def deactivate_heating(self):
        self.heating_signal = False

    def activate_air_conditioning(self):
        self.air_conditioning_signal = True
    
    def deactivate_air_conditioning(self):
        self.air_conditioning_signal = False

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

    def update_clock(self):
        # Add one second to the simulated time
        self.simulated_time = self.simulated_time.addSecs(1)

        # Extract hour, minute, second from the simulated time
        hour = self.simulated_time.hour()
        minute = self.simulated_time.minute()
        second = self.simulated_time.second()

        # Convert to 12-hour format and set AM/PM
        am_pm = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12

        # Format the time as HH:MM:SS
        time_text = f"{hour_12:02d}:{minute:02d}:{second:02d}"

        # Update the clock LCD and the AM/PM label
        self.ui.global_clock_lcd.display(time_text)
        self.ui.am_pm_label.setText(am_pm)
    
    def to_float(self, val_str, default=0.0):
        # Helper for string->float conversion
        try:
            return float(val_str)
        except ValueError:
            return default

def main():
    app = QApplication(sys.argv)
    from train_collection import TrainCollection
    train_controller_frontend = TrainControllerFrontend(TrainCollection())
    train_controller_frontend.show()
    train_controller_frontend.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()