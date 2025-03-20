"""
Author: Iyan Nekib 
"""

import sys
import os
import time
import math

# Add the parent directory (Train folder) to sys.path.
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
from train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI

# Import the TrainCollection so we can populate the dropdown.
from train_collection import TrainCollection

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'


###############################################################################
# TRAIN MODEL APP
###############################################################################
class TrainModelApp(QMainWindow):  # type: ignore
    """
    Main application that calculates acceleration from power and grade,
    simulating deceleration and updating UI elements accordingly.
    """
    # Conversion factors and constants
    MPS_TO_MPH  = 2.23694
    KG_TO_LBS   = 2.20462
    M_TO_FT     = 3.281

    MAX_ACCEL         = 100000    # Acceleration clamping value (m/s^2)
    GRAVITY           = 9.81      # Acceleration due to gravity (m/s^2)
    EMERGENCY_DECEL   = -2.73     # Emergency braking deceleration (m/s^2)
    SERVICE_DECEL     = -1.2      # Service braking deceleration (m/s^2)
    MIN_SPEED_NO_BRAKE= 0.1       # Minimum speed when brakes are off (m/s)

    def __init__(self):
        super().__init__()
        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)

        # Create TrainCollection instance and populate with trains.
        self.train_collection = TrainCollection()
        # For demonstration purposes, create three train instances.
        for _ in range(3):
            self.train_collection.createTrain()
        self.current_train = self.train_collection.train_list[0] if self.train_collection.train_list else None

        # Setup dropdown for selecting a train model.
        self.setup_train_dropdown()

        self.testbench = TestBenchApp(self)

        # Initialize physics state variables
        self.position = 0.0
        self.actual_velocity = 0.01  # Starting velocity (~2.24 mph)
        self.prev_time = None
        self.current_acceleration = 0.0
        self.cabin_temp = 25  # Cabin temperature in Celsius

        # Initialize previous acceleration for trapezoidal integration.
        self.previous_acceleration = 0.0

        # Update physics at 10 Hz (every 100ms)
        self.timer = QTimer(self)  # type: ignore
        self.timer.timeout.connect(self.update_from_testbench)
        self.timer.start(100)

        # Clock update timer (every second)
        self.simulated_time = QTime(11, 59, 0)  # type: ignore
        self.clock_timer = QTimer(self)  # type: ignore
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # Configure emergency brake button to be checkable
        self.train_ui.button_emergency.setCheckable(True)
        self.init_failure_buttons()
        # self.train_ui.button_emergency.toggled.connect(self.mark_emergency_displayed)
        self.train_ui.button_emergency.toggled.connect(self.handle_emergency_button)

    def setup_train_dropdown(self):
        """Sets up a small, rounded dropdown and embeds it in the menuTrain_ID_1 menu."""
        # Create the combo box.
        self.train_dropdown = QComboBox()
        self.train_dropdown.setFixedSize(120, 25)
        # Populate the combo box.
        for idx, train in enumerate(self.train_collection.train_list):
            self.train_dropdown.addItem(getattr(train, "name", f"Train ID {idx+1}"))
        self.train_dropdown.currentIndexChanged.connect(self.on_train_selection_changed)

        # Create a widget action and set the dropdown as its widget.
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(self.train_dropdown)
        # Add the widget action to the preexisting menu from your UI file.
        self.train_ui.menuTrain_ID_1.addAction(widget_action)

    def on_train_selection_changed(self, index):
        """Updates the current train and the menu title based on dropdown selection."""
        if 0 <= index < len(self.train_collection.train_list):
            self.current_train = self.train_collection.train_list[index]
            # Update the menu title to show the correct train ID (e.g., "Train ID 1", "Train ID 2", ...)
            self.train_ui.menuTrain_ID_1.setTitle(f"Train ID {index + 1}")
            # Optionally update other UI elements if needed.
            if hasattr(self.train_ui, "currentTrainLabel"):
                self.train_ui.currentTrainLabel.setText(f"Selected: {self.train_dropdown.currentText()}")


    ###############################################################################
    # HELPER FUNCTIONS
    ###############################################################################
    def read_wayside_data(ui, to_float_func):
        # Read and convert wayside inputs from UI.
        commanded_power = to_float_func(ui.CommandedPower.text(), 0.0)  # (Watts)
        
        # Cap the power at 60%
        if commanded_power > 120000:  # 120 kW
            commanded_power = 120000.0
        elif commanded_power < 0:
            commanded_power = 0.0

        return {
            "commanded_speed": to_float_func(ui.WaysideSpeed.text(), 0.0),  # (m/s)
            "authority":       to_float_func(ui.WaysideAuthority.text(), 0.0),
            "commanded_power": commanded_power,  # (Watts)
            "speed_limit":     to_float_func(ui.SpeedLimit.text(), 0.0),  # (m/s)
            "beacon_data":     ui.BeaconData.text(),
        }

    def read_lights_doors_data(ui):
        # Read the state of various lights, doors, and signals from UI.
        return {
            "service_brakes": ui.ServiceBrakes.isChecked(),
            "ext_lights":     ui.ExtLights.isChecked(),
            "int_lights":     ui.IntLights.isChecked(),
            "left_doors":     ui.LeftDoors.isChecked(),
            "right_doors":    ui.RightDoors.isChecked(),
            "announcements":  ui.Announcements.text(),
            "ac_signal":      ui.ACSignal.isChecked(),
            "heat_signal":    ui.HeatingSignal.isChecked()
        }

    def read_train_physical_data(ui, to_float_func):
        """
        Reads train physical attributes in metric units.
        Length, height, and width are converted to feet later in the main logic.
        The grade is capped at 60%.
        """
        base_mass_kg = to_float_func(ui.MassVehicle.text(), 37103.86)
        passenger_count = to_float_func(ui.PassengerCount.text(), 0.0)
        crew_count = to_float_func(ui.CrewCount.text(), 2.0)
        added_passenger_mass = passenger_count * 70.0
        added_crew_mass = crew_count * 70.0

        length_m = to_float_func(ui.LengthVehicle.text(), 32.2)  # default value if empty
        height_m = to_float_func(ui.HeightVehicle.text(), 3.42)
        width_m  = to_float_func(ui.WidthVehicle.text(), 2.65)
        grade_percent = to_float_func(ui.GradePercent.text(), 0.0)
        temperature = to_float_func(ui.Temperature.text(), 25.0)

        # Cap the grade at 60%
        if grade_percent > 60:
            grade_percent = 60.0
        elif grade_percent < 0:
            grade_percent = 0.0

        return {
            "length_m":        length_m,
            "height_m":        height_m,
            "width_m":         width_m,
            "grade":           grade_percent,  # e.g., 2 means 2% grade
            "mass_kg":         base_mass_kg + added_passenger_mass + added_crew_mass,
            "passenger_count": passenger_count,
            "crew_count":      crew_count,
            "temperature":     temperature
        }

    ###############################################################################
    # HELPER FUNCTIONS END
    ###############################################################################

    def update_from_testbench(self):
        """Reads inputs from the testbench, updates physics, and refreshes UI."""
        current_time = QDateTime.currentMSecsSinceEpoch()  # type: ignore
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0  # time step in seconds
        self.prev_time = current_time

        # Read inputs from the testbench UI.
        wayside_data, lights_doors_data, train_data = self.testbench.read_inputs()

        # Extract commanded values and physical parameters.
        commanded_speed   = wayside_data["commanded_speed"]
        wayside_authority = wayside_data["authority"]
        commanded_power_watts = wayside_data["commanded_power"]
        commanded_power_kw = commanded_power_watts / 1000.0
        speed_limit       = wayside_data["speed_limit"]

        mass_kg  = train_data["mass_kg"]
        mass_lbs = mass_kg * self.KG_TO_LBS
        grade    = train_data["grade"]

        # Convert dimensions from meters to feet.
        length_ft = train_data["length_m"] * self.M_TO_FT
        height_ft = train_data["height_m"] * self.M_TO_FT
        width_ft  = train_data["width_m"]  * self.M_TO_FT

        try:
            # Use a minimum effective velocity to avoid dividing by (or near) zero.
            v_eff = self.actual_velocity if self.actual_velocity > 0.1 else 0.1
            dyn_force = commanded_power_watts / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        theta = math.atan(grade / 100.0)  # Convert grade percent to angle (radians)
        grav_force = mass_kg * self.GRAVITY * math.sin(theta)

        net_force = dyn_force - grav_force
        a_base = net_force / mass_kg  # (m/s^2)

        if self.train_ui.button_emergency.isChecked():
            target_a = self.EMERGENCY_DECEL - self.GRAVITY * math.sin(theta)
            self.current_acceleration = target_a
        elif lights_doors_data["service_brakes"]:
            target_a = self.SERVICE_DECEL - self.GRAVITY * math.sin(theta)
            ramp_rate = 1.0  # m/s^3
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)
        else:
            target_a = a_base
            ramp_rate = 1.0  # m/s^3
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)

        a = self.current_acceleration
        if a > self.MAX_ACCEL:
            a = self.MAX_ACCEL
        elif a < -self.MAX_ACCEL:
            a = -self.MAX_ACCEL

        old_velocity = self.actual_velocity
        new_velocity = old_velocity + (dt / 2.0) * (a + self.previous_acceleration)
        if new_velocity < 0:
            new_velocity = 0

        threshold = 0.0001
        if commanded_speed < threshold and commanded_power_watts < threshold:
            a = 0
            new_velocity = 0

        self.previous_acceleration = a
        self.actual_velocity = new_velocity
        self.current_acceleration = a

        brake_off = (not self.train_ui.button_emergency.isChecked()) and (not lights_doors_data["service_brakes"])
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        service_brake_active = lights_doors_data["service_brakes"]
        if service_brake_active:
            a = self.SERVICE_DECEL
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: yellow; color: black;")

        degrees_per_second = 0.005  # Temperature change factor
        if lights_doors_data["heat_signal"] and not lights_doors_data["ac_signal"]:
            dtemp = degrees_per_second * dt
        elif lights_doors_data["ac_signal"] and not lights_doors_data["heat_signal"]:
            dtemp = -degrees_per_second * dt
        elif lights_doors_data["ac_signal"] and lights_doors_data["heat_signal"]:
            dtemp = 0.0
        else:
            dtemp = 0.0005
        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32  # Convert to °F

        velocity_mph   = self.actual_velocity * self.MPS_TO_MPH
        cmd_speed_mph  = commanded_speed * self.MPS_TO_MPH
        limit_mph      = speed_limit * self.MPS_TO_MPH
        acceleration_fts2 = self.current_acceleration * 3.281  # ft/s^2

        self.train_ui.AccValue.display(acceleration_fts2)
        self.train_ui.SpeedValue.display(velocity_mph)
        self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
        self.train_ui.SpeedLimitValue.display(limit_mph)
        self.train_ui.PowerValue.display(commanded_power_kw)
        self.train_ui.MassVehicleValue.display(mass_lbs)
        self.train_ui.PassengerCountValue.display(train_data["passenger_count"])
        self.train_ui.CrewCountValue.display(train_data["crew_count"])
        self.train_ui.LengthVehicleValue.display(length_ft)
        self.train_ui.HeightValue.display(height_ft)
        self.train_ui.WidthValue.display(width_ft)

        if hasattr(self.train_ui, "Announcement_2"):
            announcements_str = lights_doors_data["announcements"]
            self.train_ui.Announcement_2.setText(announcements_str)
            self.train_ui.Announcement_2.setStyleSheet("font-size: 20px; font-weight: bold;")

        if hasattr(self.train_ui, "Temperature"):
            self.train_ui.Temperature.setText(f"{display_temp:.2f} °F")
            self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

        if hasattr(self.train_ui, "GradePercentage"):
            self.train_ui.GradePercentageValue.display(grade)

        if lights_doors_data["ext_lights"]:
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: yellow; color: black;")

        if lights_doors_data["int_lights"]:
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: yellow; color: black;")

        if lights_doors_data["left_doors"]:
            self.train_ui.LeftDoorClosed.setStyleSheet("background-color: none; color: black;")
            self.train_ui.LeftDoorOpen.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.train_ui.LeftDoorOpen.setStyleSheet("background-color: none; color: black;")
            self.train_ui.LeftDoorClosed.setStyleSheet("background-color: yellow; color: black;")

        if lights_doors_data["right_doors"]:
            self.train_ui.RightDoorClosed.setStyleSheet("background-color: none; color: black;")
            self.train_ui.RightDoorOpen.setStyleSheet("background-color: yellow; color: black;")
        else:
            self.train_ui.RightDoorOpen.setStyleSheet("background-color: none; color: black;")
            self.train_ui.RightDoorClosed.setStyleSheet("background-color: yellow; color: black;")

        self.testbench.update_status()

    def init_failure_buttons(self):
        """Initializes the 6 failure buttons and makes each pair mutually exclusive."""
        self.train_ui.Enabled1.setCheckable(True)
        self.train_ui.Disabled1.setCheckable(True)
        self.train_ui.Enabled2.setCheckable(True)
        self.train_ui.Disabled2.setCheckable(True)
        self.train_ui.Enabled3.setCheckable(True)
        self.train_ui.Disabled3.setCheckable(True)

        self.failure_group1 = QButtonGroup(self)  # type: ignore
        self.failure_group1.setExclusive(True)
        self.failure_group1.addButton(self.train_ui.Enabled1)
        self.failure_group1.addButton(self.train_ui.Disabled1)

        self.failure_group2 = QButtonGroup(self)  # type: ignore
        self.failure_group2.setExclusive(True)
        self.failure_group2.addButton(self.train_ui.Enabled2)
        self.failure_group2.addButton(self.train_ui.Disabled2)

        self.failure_group3 = QButtonGroup(self)  # type: ignore
        self.failure_group3.setExclusive(True)
        self.failure_group3.addButton(self.train_ui.Enabled3)
        self.failure_group3.addButton(self.train_ui.Disabled3)

        self.train_ui.Disabled1.setChecked(True)
        self.train_ui.Disabled2.setChecked(True)
        self.train_ui.Disabled3.setChecked(True)

        self.failure_group1.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("BrakeFailure", btn))
        self.failure_group2.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("SignalFailure", btn))
        self.failure_group3.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("EngineFailure", btn))

    def on_failure_group_toggled(self, failure_type, button):
        new_status = button.text()
        if failure_type == "BrakeFailure":
            self.testbench.ui.BrakeFailure.setText(new_status)
        elif failure_type == "SignalFailure":
            self.testbench.ui.SignalFailure.setText(new_status)
        elif failure_type == "EngineFailure":
            self.testbench.ui.EngineFailure.setText(new_status)
                
    def handle_emergency_button(self, pressed: bool):
        if not self.train_ui.button_emergency.isEnabled():
            return
        if pressed:
            self.train_ui.button_emergency.setEnabled(False)
            self.testbench.ui.PEmergencyStop.setText("Enabled")
            self.testbench.ui.ServiceBrakes.setChecked(False)
            self.testbench.ui.ServiceBrakes.setEnabled(False)
            self.testbench.ui.EmergencyStop.setEnabled(True)
            self.testbench.ui.EmergencyStop.setChecked(True)
            self.testbench.ui.TrainDriver.setChecked(True)
            self.testbench.ui.TrainDriver.setEnabled(False)
        else:
            self.testbench.ui.PEmergencyStop.setText("Disabled")
            self.testbench.ui.ServiceBrakes.setEnabled(True)

    def update_clock(self):
        self.simulated_time = self.simulated_time.addSecs(1)
        hour = self.simulated_time.hour()
        minute = self.simulated_time.minute()
        am_pm = "AM" if hour < 12 else "PM"
        hour_12 = hour % 12
        if hour_12 == 0:
            hour_12 = 12
        time_text = f"{hour_12:02d}:{minute:02d}"
        self.train_ui.Clock_12.display(time_text)
        self.train_ui.AM_PM.setText(am_pm)

    def to_float(self, val_str, default=0.0):
        try:
            return float(val_str)
        except ValueError:
            return default


###############################################################################
# TESTBENCH APP
###############################################################################
class TestBenchApp(QMainWindow):  # type: ignore
    def __init__(self, train_app):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_app = train_app
        
        self.ui.PEmergencyStop.setText("Disabled")
        self.ui.BrakeFailure.setText("Disabled")
        self.ui.SignalFailure.setText("Disabled")
        self.ui.EngineFailure.setText("Disabled")
        
        self.ui.EmergencyStop.setCheckable(True)
        self.ui.EmergencyStop.setEnabled(False)
        self.ui.EmergencyStop.setChecked(False)
        self.ui.EmergencyStop.toggled.connect(self.handle_emergency_release)
        
        self.ui.TrainDriver.toggled.connect(self.handle_train_driver)

    def handle_train_driver(self, checked: bool):
        if checked:
            self.train_app.train_ui.button_emergency.setChecked(True)
            self.train_app.train_ui.button_emergency.setEnabled(False)
            self.ui.PEmergencyStop.setText("Enabled")
            self.ui.EmergencyStop.setEnabled(True)
            self.ui.EmergencyStop.setChecked(True)
            self.ui.TrainDriver.setEnabled(False)
        else:
            self.train_app.train_ui.button_emergency.setEnabled(True)
            self.train_app.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)

    def handle_emergency_release(self, checked: bool):
        if not checked:
            self.train_app.train_ui.button_emergency.setEnabled(True)
            self.train_app.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)
            self.ui.TrainDriver.setEnabled(True)
            self.ui.TrainDriver.setChecked(False)

    def read_inputs(self):
        f = self.train_app.to_float
        wayside_data        = TrainModelApp.read_wayside_data(self.ui, f)
        lights_doors_data   = TrainModelApp.read_lights_doors_data(self.ui)
        train_physical_data = TrainModelApp.read_train_physical_data(self.ui, f)
        return wayside_data, lights_doors_data, train_physical_data

    def update_status(self):
        cmd_speed_str = self.ui.WaysideSpeed.text()
        cmd_speed_val = self.train_app.to_float(cmd_speed_str, -999)
        cmd_speed_val_mph = cmd_speed_val * self.train_app.MPS_TO_MPH
        model_cmd_speed = self.train_app.train_ui.CommandedSpeedValue.value()
        if abs(cmd_speed_val_mph - model_cmd_speed) < 0.0001:
            self.ui.WaysideSpeed_2.setText(f"{(cmd_speed_val_mph):.2f}")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")
        
        auth_str = self.ui.WaysideAuthority.text()
        auth_val = self.train_app.to_float(auth_str, 0.0)
        if abs(auth_val) > 0.0001:
            self.ui.WaysideAuthority_2.setText(f"{(auth_val * 3.281):.2f}")
        else:
            self.ui.WaysideAuthority_2.setText("Not Displayed")
        
        speed_limit_str = self.ui.SpeedLimit.text()
        speed_limit_val = self.train_app.to_float(speed_limit_str, 0.0)
        speed_limit_val_mph = speed_limit_val * self.train_app.MPS_TO_MPH
        model_speed_limit = self.train_app.train_ui.SpeedLimitValue.value()
        if abs(speed_limit_val_mph - model_speed_limit) < 0.0001:
            self.ui.SpeedLimit_2.setText(f"{speed_limit_val_mph:.2f}")
        else:
            self.ui.SpeedLimit_2.setText("Not Displayed")
        
        speed_ui = self.train_app.train_ui.SpeedValue.value()
        internal_mph = self.train_app.actual_velocity * self.train_app.MPS_TO_MPH
        if abs(internal_mph - speed_ui) < 0.0001:
            self.ui.ActualVelocity.setText(f"{internal_mph:.2f}")
        else:
            self.ui.ActualVelocity.setText("Not Displayed")
            
        self.ui.Temperature.setText(self.train_app.train_ui.Temperature.text())


###############################################################################
# MAIN
###############################################################################
def main():
    app = QApplication(sys.argv)  # type: ignore
    train_model_app = TrainModelApp()
    train_model_app.show()
    train_model_app.testbench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
