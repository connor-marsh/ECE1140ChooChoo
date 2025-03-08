"""
Author: Iyan Nekib 
"""

import sys
import os
import time
import math

from PyQt5 import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QButtonGroup
from PyQt5.QtGui import *
from PyQt5.QtCore import QTimer, QTime, QDateTime

from train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
from train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI


os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'


###############################################################################
# HELPER FUNCTIONS
###############################################################################
def read_wayside_data(ui, to_float_func):
    # Read and convert wayside inputs from UI.
    return {
        "commanded_speed": to_float_func(ui.WaysideSpeed.text(), 0.0),   # (m/s)
        "authority":       to_float_func(ui.WaysideAuthority.text(), 0.0),
        "commanded_power": to_float_func(ui.CommandedPower.text(), 0.0),  # (Watts)
        "speed_limit":     to_float_func(ui.SpeedLimit.text(), 0.0),      # (m/s)
        "beacon_data":     ui.BeaconData.text(),
    }

def read_lights_doors_data(controller, ui, fromTestbench):
    # Read the state of various lights, doors, and signals from UI.
    if fromTestbench:
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
    else:
        return {
            "service_brakes": controller.service_brake,
            "ext_lights":     controller.headlights,
            "int_lights":     controller.interior_lights,
            "left_doors":     controller.door_left,
            "right_doors":    controller.door_right,
            "announcements":  controller.next_station,
            "ac_signal":      controller.air_conditioning_signal,
            "heat_signal":    controller.heating_signal
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

    length_m = to_float_func(ui.LengthVehicle.text(), 32.2)   # default value if empty
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
# TESTBENCH APP
###############################################################################
class TestBenchApp(QMainWindow):
    def __init__(self, train_app):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_app = train_app
        
        # Set default texts for indicators on the testbench.
        self.ui.PEmergencyStop.setText("Disabled")
        self.ui.BrakeFailure.setText("Disabled")
        self.ui.SignalFailure.setText("Disabled")
        self.ui.EngineFailure.setText("Disabled")
        
        # Configure the testbench emergency release checkbox:
        self.ui.EmergencyStop.setCheckable(True)
        self.ui.EmergencyStop.setEnabled(False)   # Initially disabled
        self.ui.EmergencyStop.setChecked(False)     # Initially not active
        self.ui.EmergencyStop.toggled.connect(self.handle_emergency_release)
        
        # Connect the TrainDriver checkbox toggled signal.
        self.ui.TrainDriver.toggled.connect(self.handle_train_driver)

    def handle_train_driver(self, checked: bool):
        """
        When the Train Driver checkbox is checked, engage the emergency mode
        as if the emergency button were pressed—lock the main UI emergency button 
        (set it checked and disabled) and update the testbench indicator.
        When unchecked, release the emergency.
        """
        if checked:
            # Engage emergency mode.
            self.train_app.train_ui.button_emergency.setChecked(True)
            self.train_app.train_ui.button_emergency.setEnabled(False)
            self.ui.PEmergencyStop.setText("Enabled")
            # Also ensure the testbench emergency release control is enabled and active.
            self.ui.EmergencyStop.setEnabled(True)
            self.ui.EmergencyStop.setChecked(True)
            # Disable the Train Driver checkbox so it cannot be manually unchecked.
            self.ui.TrainDriver.setEnabled(False)
        else:
            # Release emergency mode.
            self.train_app.train_ui.button_emergency.setEnabled(True)
            self.train_app.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)

    def handle_emergency_release(self, checked: bool):
        # When the testbench checkbox is unchecked, release the emergency.
        if not checked:
            # Re-enable the main UI emergency button and uncheck it.
            self.train_app.train_ui.button_emergency.setEnabled(True)
            self.train_app.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            # Disable the testbench checkbox again.
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)
            # Re-enable the Train Driver checkbox and reset its state.
            self.ui.TrainDriver.setEnabled(True)
            self.ui.TrainDriver.setChecked(False)

    def read_inputs(self):
        # Get inputs from UI, converting as needed.
        f = self.train_app.to_float
        wayside_data        = read_wayside_data(self.ui, f)
        lights_doors_data   = read_lights_doors_data(self.train_app.controller, self.ui, self.train_app.fromTestbench)
        train_physical_data = read_train_physical_data(self.ui, f)
        return wayside_data, lights_doors_data, train_physical_data

    def update_status(self):
        """Checks if the Train Model UI is displaying correct values."""
        # Check commanded speed.
        cmd_speed_str = self.ui.WaysideSpeed.text()
        cmd_speed_val = self.train_app.to_float(cmd_speed_str, -999)
        # Convert the testbench commanded speed from m/s to mph.
        cmd_speed_val_mph = cmd_speed_val * self.train_app.MPS_TO_MPH
        model_cmd_speed = self.train_app.train_ui.CommandedSpeedValue.value()
        if abs(cmd_speed_val_mph - model_cmd_speed) < 0.0001:
            self.ui.WaysideSpeed_2.setText(f"{(cmd_speed_val_mph):.2f}")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")
        
        # Check authority signal.
        auth_str = self.ui.WaysideAuthority.text()  # Authority input.
        auth_val = self.train_app.to_float(auth_str, 0.0)
        if abs(auth_val) > 0.0001:
            self.ui.WaysideAuthority_2.setText(f"{(auth_val * 3.281):.2f}")
        else:
            self.ui.WaysideAuthority_2.setText("Not Displayed")
        
        # Check speed limit.
        speed_limit_str = self.ui.SpeedLimit.text()
        speed_limit_val = self.train_app.to_float(speed_limit_str, 0.0)
        # Convert the testbench speed limit from m/s to mph.
        speed_limit_val_mph = speed_limit_val * self.train_app.MPS_TO_MPH
        model_speed_limit = self.train_app.train_ui.SpeedLimitValue.value()
        if abs(speed_limit_val_mph - model_speed_limit) < 0.0001:
            self.ui.SpeedLimit_2.setText(f"{speed_limit_val_mph:.2f}")
        else:
            self.ui.SpeedLimit_2.setText("Not Displayed")
        
        # Check actual velocity.
        speed_ui = self.train_app.train_ui.SpeedValue.value()  # mph from UI.
        internal_mph = self.train_app.actual_velocity * self.train_app.MPS_TO_MPH
        if abs(internal_mph - speed_ui) < 0.0001:
            self.ui.ActualVelocity.setText(f"{internal_mph:.2f}")
        else:
            self.ui.ActualVelocity.setText("Not Displayed")
            
        # Check Temperature
        self.ui.Temperature.setText(self.train_app.train_ui.Temperature.text())

###############################################################################
# TRAIN MODEL APP
###############################################################################
class TrainModelApp(QMainWindow):
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

        self.testbench = TestBenchApp(self)
        self.fromTestbench = True
        self.controller = TrainController(self)

        # Initialize physics state variables
        self.position = 0.0
        self.actual_velocity = 0.01  # Starting velocity (~2.24 mph)
        self.prev_time = None
        self.current_acceleration = 0.0
        self.cabin_temp = 25 # Cabin temperature in Celsius

        # Initialize previous acceleration for trapezoidal integration.
        self.previous_acceleration = 0.0

        # Update physics at 10 Hz (every 100ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        # Clock update timer (every second)
        self.simulated_time = QTime(11, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # Shared emergency flag
        self.emergency_brake = False
        self.emergency_source = None  # Can be "model" or "controller"

        # Configure emergency brake button to be checkable
        self.train_ui.button_emergency.setCheckable(True)
        self.init_failure_buttons()
        # self.train_ui.button_emergency.toggled.connect(self.mark_emergency_displayed)
        self.train_ui.button_emergency.toggled.connect(self.handle_emergency_button)

    def update(self):
        """Reads inputs from the testbench, updates physics, and refreshes UI."""
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0  # time step in seconds
        self.prev_time = current_time

        # Read inputs from the testbench UI
        wayside_data, lights_doors_data, train_data = self.testbench.read_inputs()

        # Extract commanded values and physical parameters
        commanded_speed   = wayside_data["commanded_speed"]
        wayside_authority = wayside_data["authority"]
        commanded_power_watts = wayside_data["commanded_power"] # Iyan - Does this need to be checked with the controller Power?
        
        speed_limit       = wayside_data["speed_limit"]

        mass_kg  = train_data["mass_kg"]
        mass_lbs = mass_kg * self.KG_TO_LBS
        grade    = train_data["grade"]
        # start by sending data to the train controller
        self.controller.commanded_wayside_speed = commanded_speed
        self.controller.commanded_authority = wayside_authority
        self.controller.speed_limit = speed_limit
        self.controller.actual_speed = self.actual_velocity

        # Convert dimensions from meters to feet
        length_ft = train_data["length_m"] * self.M_TO_FT
        height_ft = train_data["height_m"] * self.M_TO_FT
        width_ft  = train_data["width_m"]  * self.M_TO_FT

        # # Before calculating dyn_force, if brakes are active, zero out the power.
        # if self.train_ui.button_emergency.isChecked() or lights_doors_data["service_brakes"]:
        #     commanded_power_watts = 0

        # Calculate dynamic force component   
        commanded_power_watts = self.controller.commanded_power      
        try:
            # Use a minimum effective velocity to avoid dividing by (or near) zero.
            v_eff = self.actual_velocity if self.actual_velocity > 0.1 else 0.1
            dyn_force = commanded_power_watts / v_eff
        except ZeroDivisionError:
            dyn_force = 1000.0

        # Calculate gravitational force component
        theta = math.atan(grade / 100.0)  # Convert grade percent to angle (radians)
        grav_force = mass_kg * self.GRAVITY * math.sin(theta)

        # Net force and basic acceleration (a_base) from Newton's second law.
        net_force = dyn_force - grav_force
        a_base = net_force / mass_kg  # (m/s^2)

        if self.train_ui.button_emergency.isChecked():
            # When braking, set acceleration to the brake deceleration adjusted by grade.
            target_a = self.EMERGENCY_DECEL - self.GRAVITY * math.sin(theta)
            # Immediately set current acceleration to target to avoid ramping from previous state.
            self.current_acceleration = target_a
        elif lights_doors_data["service_brakes"]:
            target_a = self.SERVICE_DECEL - self.GRAVITY * math.sin(theta)
            ramp_rate = 1.0  # m/s^3, adjust for smoother or faster transitions
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)
        else:
            # Otherwise, ramp current acceleration toward the dynamic target.
            target_a = a_base
            ramp_rate = 1.0  # m/s^3
            accel_diff = target_a - self.current_acceleration
            max_delta = ramp_rate * dt
            if abs(accel_diff) < max_delta:
                self.current_acceleration = target_a
            else:
                self.current_acceleration += math.copysign(max_delta, accel_diff)

        # Use the smoothly updated acceleration for integration.
        a = self.current_acceleration

        # Clamp the acceleration to avoid unrealistic values.
        if a > self.MAX_ACCEL:
            a = self.MAX_ACCEL
        elif a < -self.MAX_ACCEL:
            a = -self.MAX_ACCEL

        # Update velocity using trapezoidal integration.
        # v_n = v_(n-1) + (dt/2) * (a_n + a_(n-1))
        old_velocity = self.actual_velocity
        new_velocity = old_velocity + (dt / 2.0) * (a + self.previous_acceleration)
        if new_velocity < 0:
            a = 0
            new_velocity = 0

        # Connor Marsh - I dont think this is needed
        # If both commanded speed and power are near zero, force zero acceleration and velocity.
        # threshold = 0.0001
        # if commanded_speed < threshold and commanded_power_watts < threshold:
        #     a = 0
        #     new_velocity = 0

        # Update previous acceleration for the next cycle.
        self.previous_acceleration = a

        # Update simulation state.
        self.actual_velocity = new_velocity
        self.current_acceleration = a

        # Ensure minimum velocity when brakes are off.
        brake_off = (not self.train_ui.button_emergency.isChecked()) and (not lights_doors_data["service_brakes"])
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        # TEMPERATURE SETUP:
        # Define the environmental (ambient) temperature of the train car (in Celsius)
        T_env = 25.0

        # Get desired target temperature from the controller (in Celsius)
        T_target = self.controller.desired_temperature

        # Calculate the error between the target and the current cabin temperature.
        error_temp = T_target - self.cabin_temp
        threshold = 1.0  # in Celsius; defines when to switch from active HVAC to ambient drift

        if abs(error_temp) > threshold:
            # Active HVAC: drive the temperature rapidly toward the target.
            k_active = 0.005  # gain for active adjustment (tune as needed)
            dtemp = k_active * error_temp * dt
        else:
            # When near the target, HVAC influence reduces and the temperature drifts slowly toward T_env.
            k_env = 0.01  # gain for natural drift (much smaller than active gain)
            dtemp = k_env * (T_env - self.cabin_temp) * dt

        self.cabin_temp += dtemp
        display_temp = (self.cabin_temp * 1.8) + 32  # Convert Celsius to Fahrenheit

        # Service brake UI updates.
        service_brake_active = lights_doors_data["service_brakes"] # or (speed_limit > 0 and self.actual_velocity > speed_limit)
        if service_brake_active:
            a = self.SERVICE_DECEL
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: yellow; color: black;")
            # self.train_ui.button_emergency.setEnabled(False)
        else:
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: yellow; color: black;")
            # self.train_ui.button_emergency.setEnabled(True)

        # Update UI fields.
        velocity_mph   = self.actual_velocity * self.MPS_TO_MPH
        cmd_speed_mph  = commanded_speed * self.MPS_TO_MPH
        limit_mph      = speed_limit * self.MPS_TO_MPH
        acceleration_fts2 = self.current_acceleration * 3.281  # Convert to ft/s^2

        commanded_power_kw = commanded_power_watts / 1000.0

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
            # self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

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

        # Finalize testbench status updates.
        self.testbench.update_status()

    def init_failure_buttons(self):
        """Initializes the 6 failure buttons and makes each pair mutually exclusive."""
        # Make all buttons checkable
        self.train_ui.Enabled1.setCheckable(True)
        self.train_ui.Disabled1.setCheckable(True)
        self.train_ui.Enabled2.setCheckable(True)
        self.train_ui.Disabled2.setCheckable(True)
        self.train_ui.Enabled3.setCheckable(True)
        self.train_ui.Disabled3.setCheckable(True)

        # Create a button group for each pair and set them to be exclusive.
        self.failure_group1 = QButtonGroup(self) # type: ignore
        self.failure_group1.setExclusive(True)
        self.failure_group1.addButton(self.train_ui.Enabled1)
        self.failure_group1.addButton(self.train_ui.Disabled1)

        self.failure_group2 = QButtonGroup(self) # type: ignore
        self.failure_group2.setExclusive(True)
        self.failure_group2.addButton(self.train_ui.Enabled2)
        self.failure_group2.addButton(self.train_ui.Disabled2)

        self.failure_group3 = QButtonGroup(self) # type: ignore
        self.failure_group3.setExclusive(True)
        self.failure_group3.addButton(self.train_ui.Enabled3)
        self.failure_group3.addButton(self.train_ui.Disabled3)

        # Set the default state: each failure is disabled.
        self.train_ui.Disabled1.setChecked(True)
        self.train_ui.Disabled2.setChecked(True)
        self.train_ui.Disabled3.setChecked(True)

        # Optionally, connect the buttonClicked signals to update your testbench UI.
        self.failure_group1.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("BrakeFailure", btn))
        self.failure_group2.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("SignalFailure", btn))
        self.failure_group3.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("EngineFailure", btn))

    def on_failure_group_toggled(self, failure_type, button):
        """Updates the corresponding testbench label based on the button pressed."""
        new_status = button.text()
        is_enabled = (new_status == "Enabled")
        if failure_type == "BrakeFailure":
            self.testbench.ui.BrakeFailure.setText(new_status)
            self.controller.brake_failure = is_enabled
        elif failure_type == "SignalFailure":
            self.testbench.ui.SignalFailure.setText(new_status)
            self.controller.signal_failure = is_enabled
        elif failure_type == "EngineFailure":
            self.testbench.ui.EngineFailure.setText(new_status)
            self.controller.engine_failure = is_enabled
        # If any failure is enabled, force emergency.
        if self.controller.brake_failure or self.controller.signal_failure or self.controller.engine_failure:
            # Set the emergency source to "controller" so that the Controller can later release it.
            self.emergency_source = "controller"
            self.set_emergency_state(True)
            
    def handle_emergency_button(self, pressed: bool):
        """
        This handler is attached to the Train Model UI emergency button.
        It only allows engaging emergency (i.e. when pressed, it locks emergency on).
        Attempts to disable it from the Model UI (i.e. unchecking) are ignored.
        """
        if pressed:
            self.emergency_source = "model"
            self.set_emergency_state(True)
        else:
            # Ignore disable attempts from the Model UI.
            self.set_emergency_state(True)

    def set_emergency_state(self, state: bool):
        """
        Update the emergency flag and synchronize both the Model and Controller UIs.
        
        - If the emergency was triggered from the Model (emergency_source == "model"), then
        an attempt to disable emergency (state==False) is ignored if any failure is active.
        - If triggered via the Controller (emergency_source == "controller"), toggle the emergency state
        exactly as requested.
        """
        # If triggered from the Model, ignore disable attempts when failures are active.
        if self.emergency_source == "model":
            # Only override disable attempts if emergency was triggered from the Model.
            if not state:
                if (self.controller.brake_failure or 
                    self.controller.signal_failure or 
                    self.controller.engine_failure):
                    state = True  # Force emergency to remain on

        # For a Controller-triggered toggle, if trying to disable but failures are active, force emergency on.
        if self.emergency_source == "controller" and not state:
            if (self.controller.brake_failure or 
                self.controller.signal_failure or 
                self.controller.engine_failure):
                state = True

        self.emergency_brake = state

        # Update the Model emergency button.
        self.train_ui.button_emergency.blockSignals(True)
        self.train_ui.button_emergency.setChecked(state)
        if state and self.emergency_source == "model":
            # Lock the Model button so it cannot be toggled off when triggered from Model.
            self.train_ui.button_emergency.setEnabled(False)
        else:
            self.train_ui.button_emergency.setEnabled(True)
        self.train_ui.button_emergency.blockSignals(False)

        # Update the Controller emergency button.
        if hasattr(self.controller, 'ui'):
            self.controller.ui.emergency_button.blockSignals(True)
            self.controller.ui.emergency_button.setChecked(state)
            # Always allow the Controller button to be enabled so the user can toggle it normally.
            self.controller.ui.emergency_button.setEnabled(True)
            self.controller.ui.emergency_button.blockSignals(False)

    def update_clock(self):
        """Update the simulated clock display every second."""
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
        """Convert a string to a float, returning a default value if conversion fails."""
        try:
            return float(val_str)
        except ValueError:
            return default


###############################################################################
# MAIN
###############################################################################
def main():
    
    app = QApplication(sys.argv)
    train_model_app = TrainModelApp()
    if __name__ == "__main__":
        train_model_app.fromTestbench=False
    train_model_app.show()
    train_model_app.controller.show()
    train_model_app.testbench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    from train_controller_main import TrainControllerWindow as TrainController
    main()
