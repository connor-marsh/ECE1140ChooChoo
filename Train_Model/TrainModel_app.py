import sys
import os
import time
import math

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import *

from TrainModel_UI_Iteration_1 import Ui_MainWindow as TrainModelUI
from TrainModel_UI_TestBench_Iteration_1 import Ui_TestMainWindow as TestBenchUI

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'


###############################################################################
# HELPER FUNCTIONS
###############################################################################
def read_wayside_data(ui, to_float_func):
    return {
        "commanded_speed": to_float_func(ui.WaysideSpeed.text(), 0.0),   # (m/s)
        "authority":       to_float_func(ui.WaysideAuthority.text(), 0.0),
        "commanded_power": to_float_func(ui.CommandedPower.text(), 0.0), # (Watts)
        "speed_limit":     to_float_func(ui.SpeedLimit.text(), 0.0),     # (m/s)
        "beacon_data":     ui.BeaconData.text(),
    }

def read_lights_doors_data(ui):
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
    Reads train physical attributes in metric (unless otherwise noted).
    We'll convert length, height, and width to feet in the main logic.
    Grade is a percent capped at 60.
    """
    base_mass_kg = to_float_func(ui.MassVehicle.text(), 37103.86)
    passenger_count = to_float_func(ui.PassengerCount.text(), 0.0)
    crew_count = to_float_func(ui.CrewCount.text(), 2.0)
    added_passenger_mass = passenger_count * 70.0
    added_crew_mass = crew_count * 70.0

    length_m = to_float_func(ui.LengthVehicle.text(), 32.2)   # default if empty
    height_m = to_float_func(ui.HeightVehicle.text(), 3.42)
    width_m  = to_float_func(ui.WidthVehicle.text(), 2.65)
    grade_percent = to_float_func(ui.GradePercent.text(), 0.0)

    # cap the grade at 60%
    if grade_percent > 60:
        grade_percent = 60.0
    elif grade_percent < 0:
        grade_percent = 0.0

    return {
        "length_m":   length_m,
        "height_m":   height_m,
        "width_m":    width_m,
        "grade":      grade_percent,   # e.g. 2 => 2% grade
        "mass_kg":    base_mass_kg + added_passenger_mass + added_crew_mass,
        "passenger_count": passenger_count,
        "crew_count":      crew_count
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

    def read_inputs(self):
        f = self.train_app.to_float
        wayside_data        = read_wayside_data(self.ui, f)
        lights_doors_data   = read_lights_doors_data(self.ui)
        train_physical_data = read_train_physical_data(self.ui, f)
        return wayside_data, lights_doors_data, train_physical_data

    def update_status(self):
        """Checks if the Train Model UI is displaying correct values."""
        # compare commanded speed vs. displayed speed
        cmd_speed_str = self.ui.WaysideSpeed.text()
        cmd_speed_val = self.train_app.to_float(cmd_speed_str, -999)
        model_cmd_speed = self.train_app.train_ui.CommandedSpeedValue.value()
        if abs(cmd_speed_val - model_cmd_speed) < 0.0001:
            self.ui.WaysideSpeed_2.setText("Displayed")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")

        # check wayside authority signal:
        auth_str = self.ui.WaysideAuthority.text()  # assuming this is where the authority is input
        auth_val = self.train_app.to_float(auth_str, 0.0)
        # Here, we assume that a nonzero value means the signal is present
        if abs(auth_val) > 0.0001:
            self.ui.WaysideAuthority_2.setText("Displayed")
        else:
            self.ui.WaysideAuthority_2.setText("Not Displayed")

        # compare actual velocity in mph
        if hasattr(self.train_app.train_ui, "SpeedValue"):
            speed_ui = self.train_app.train_ui.SpeedValue.value()  # mph shown in UI
            internal_mph = self.train_app.actual_velocity * self.train_app.MPS_TO_MPH
            if abs(internal_mph - speed_ui) < 0.0001:
                self.ui.ActualVelocity.setText("Displayed")
            else:
                self.ui.ActualVelocity.setText("Not Displayed")


###############################################################################
# TRAIN MODEL APP
###############################################################################
class TrainModelApp(QMainWindow):
    """
    Main application that calculates acceleration from power & grade,
    ensures slow deceleration, and displays results in the Train Model UI.
    """
    MPS_TO_MPH  = 2.23694
    KG_TO_LBS   = 2.20462
    M_TO_FT     = 3.281

    MAX_ACCEL     = 100000     # clamp
    GRAVITY       = 9.81       # m/s^2
    EMERGENCY_DECEL = -2.73    # m/s^2
    SERVICE_DECEL   = -1.2     # m/s^2
    MIN_SPEED_NO_BRAKE = 0.1   # m/s

    def __init__(self):
        super().__init__()
        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)

        self.testbench = TestBenchApp(self)

        # physics states
        self.position   = 0.0
        self.actual_velocity = 1.0   # start ~2.24 mph
        self.prev_time  = None
        self.current_acceleration = 0.0
        self.cabin_temp = 70.0

        # 10 updates/sec
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_from_testbench)
        self.timer.start(100)

        # timer for updating the clock every second
        self.simulated_time = QTime(11, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # make emergency brake checkable
        self.train_ui.button_emergency.setCheckable(True)
        self.init_failure_buttons()
        self.train_ui.button_emergency.toggled.connect(self.mark_emergency_displayed)

    def update_from_testbench(self):
        """Reads data from testbench, updates physics, displays them."""
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0  # convert milliseconds to seconds
        self.prev_time = current_time

        wayside_data, lights_doors_data, train_data = self.testbench.read_inputs()

        commanded_speed   = wayside_data["commanded_speed"]
        wayside_authority = wayside_data["authority"]
        commanded_power_watts = wayside_data["commanded_power"]
        commanded_power_kw = commanded_power_watts / 1000.0

        speed_limit       = wayside_data["speed_limit"]

        mass_kg  = train_data["mass_kg"]
        mass_lbs = mass_kg * self.KG_TO_LBS
        grade    = train_data["grade"]

        # convert L, H, W from meters -> feet
        length_ft = train_data["length_m"] * self.M_TO_FT
        height_ft = train_data["height_m"] * self.M_TO_FT
        width_ft  = train_data["width_m"]  * self.M_TO_FT

        # net force from gravity & power
        theta = math.atan(grade / 100.0)
        grav_force = mass_kg * self.GRAVITY * math.sin(theta)

        try:
            if self.actual_velocity <= 0.0:
                dyn_force = 1000.0
            else:
                dyn_force = commanded_power_watts / self.actual_velocity
        except ZeroDivisionError:
            dyn_force = 1000.0

        net_force = dyn_force - grav_force
        a_base = net_force / mass_kg  # m/s^2

        # brake logic
        if self.train_ui.button_emergency.isChecked():
            a = self.EMERGENCY_DECEL
        elif lights_doors_data["service_brakes"]:
            a = self.SERVICE_DECEL
        else:
            a = a_base

        # clamp
        if a > self.MAX_ACCEL:
            a = self.MAX_ACCEL
        elif a < -self.MAX_ACCEL:
            a = -self.MAX_ACCEL

        # integrate velocity
        old_velocity = self.actual_velocity
        new_velocity = old_velocity + a * dt
        if new_velocity < 0:
            new_velocity = 0

        # if brake is off, ensure min speed
        brake_off = (not self.train_ui.button_emergency.isChecked()) and (not lights_doors_data["service_brakes"])
        if brake_off and new_velocity < self.MIN_SPEED_NO_BRAKE:
            new_velocity = self.MIN_SPEED_NO_BRAKE

        service_brake_active = lights_doors_data["service_brakes"] or (speed_limit > 0 and self.actual_velocity > speed_limit)

        if service_brake_active:
            a = self.SERVICE_DECEL
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: yellow; color: black;")
            self.train_ui.button_emergency.setEnabled(False)
        else:
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: yellow; color: black;")
            self.train_ui.button_emergency.setEnabled(True)

        self.actual_velocity = new_velocity
        self.current_acceleration = a

        # cabin Temp
        # e.g. ±0.05 °F / s if AC or heat
        degrees_per_second = 0.005
        dtemp = 0.0
        if lights_doors_data["heat_signal"] and not lights_doors_data["ac_signal"]:
            # increase temperature linearly by +0.05°F every 10 seconds
            dtemp = degrees_per_second * dt
        elif lights_doors_data["ac_signal"] and not lights_doors_data["heat_signal"]:
            # suppose AC is still 0.05°F every 10 seconds but downward
            dtemp = -degrees_per_second * dt
        elif lights_doors_data["ac_signal"] and lights_doors_data["heat_signal"]:
            # both on => net 0
            dtemp = 0.0
        else:
            dtemp = 0.0005  # no net change

        self.cabin_temp += dtemp

        # update UI fields
        # convert velocity to mph
        velocity_mph   = self.actual_velocity * self.MPS_TO_MPH
        cmd_speed_mph  = commanded_speed * self.MPS_TO_MPH
        limit_mph      = speed_limit * self.MPS_TO_MPH
        acceleration_fts2 = self.current_acceleration * 3.281

        # acceleration (ft/s^2)
        self.train_ui.AccValue.display(acceleration_fts2)
        # actual speed (mph)
        self.train_ui.SpeedValue.display(velocity_mph)
        # commanded speed & limit (mph)
        self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
        self.train_ui.SpeedLimitValue.display(limit_mph)
        self.train_ui.PowerValue.display(commanded_power_kw)

        # mass in lbs
        self.train_ui.MassVehicleValue.display(mass_lbs)
        # display passenger & crew
        self.train_ui.PassengerCountValue.display(train_data["passenger_count"])
        self.train_ui.CrewCountValue.display(train_data["crew_count"])

        # show length, height, width in feet
        self.train_ui.LengthVehicleValue.display(length_ft)
        self.train_ui.HeightValue.display(height_ft)
        self.train_ui.WidthValue.display(width_ft)

        # show announcements
        if hasattr(self.train_ui, "Announcement_2"):
            announcements_str = lights_doors_data["announcements"]
            self.train_ui.Announcement_2.setText(announcements_str)
            self.train_ui.Announcement_2.setStyleSheet("font-size: 20px; font-weight: bold;")

        # show cabin temp if you have a Temperature label/QLCD
        if hasattr(self.train_ui, "Temperature"):
            self.train_ui.Temperature.setText(f"{self.cabin_temp:.2f} °F")
            self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

        # show the grade if user has GradeValue
        if hasattr(self.train_ui, "GradeValue"):
            self.train_ui.GradeValue.display(grade)  # capped at 60

        if lights_doors_data["ext_lights"]:
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: green; color: white;")
        else:
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: red; color: black;")

        if lights_doors_data["int_lights"]:
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: green; color: white;")
        else:
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: red; color: black;")

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

        # TestBench finalized “Displayed?” checks
        self.testbench.update_status()

    def init_failure_buttons(self):
        """Sets checkable states for the 6 (Enabled/Disabled) buttons."""
        self.train_ui.Enabled1.setCheckable(True)
        self.train_ui.Enabled2.setCheckable(True)
        self.train_ui.Enabled3.setCheckable(True)
        self.train_ui.Disabled1.setCheckable(True)
        self.train_ui.Disabled2.setCheckable(True)
        self.train_ui.Disabled3.setCheckable(True)

        self.train_ui.Enabled1.toggled.connect(lambda checked: self.on_failure_toggled("Enabled1", checked))
        self.train_ui.Enabled2.toggled.connect(lambda checked: self.on_failure_toggled("Enabled2", checked))
        self.train_ui.Enabled3.toggled.connect(lambda checked: self.on_failure_toggled("Enabled3", checked))
        self.train_ui.Disabled1.toggled.connect(lambda checked: self.on_failure_toggled("Disabled1", checked))
        self.train_ui.Disabled2.toggled.connect(lambda checked: self.on_failure_toggled("Disabled2", checked))
        self.train_ui.Disabled3.toggled.connect(lambda checked: self.on_failure_toggled("Disabled3", checked))

    def on_failure_toggled(self, button_name, checked):
        """When a failure button is toggled, update the corresponding label in the TestBench."""
        text_to_set = "Displayed" if checked else "Not Displayed"

        if button_name == "Enabled1":
            self.testbench.ui.BrakeFailure.setText(text_to_set)
            self.train_ui.Disabled1.setEnabled(not checked)
        elif button_name == "Disabled1":
            self.testbench.ui.BrakeFailure.setText(text_to_set)
            self.train_ui.Enabled1.setEnabled(not checked)

        elif button_name == "Enabled2":
            self.testbench.ui.SignalFailure.setText(text_to_set)
            self.train_ui.Disabled2.setEnabled(not checked)
        elif button_name == "Disabled2":
            self.testbench.ui.SignalFailure.setText(text_to_set)
            self.train_ui.Enabled2.setEnabled(not checked)

        elif button_name == "Enabled3":
            self.testbench.ui.EngineFailure.setText(text_to_set)
            self.train_ui.Disabled3.setEnabled(not checked)
        elif button_name == "Disabled3":
            self.testbench.ui.EngineFailure.setText(text_to_set)
            self.train_ui.Enabled3.setEnabled(not checked)


    def mark_emergency_displayed(self, pressed: bool):
        """If the emergency brake is toggled on, set testbench label to 'Displayed'."""
        if pressed:
            self.testbench.ui.PEmergencyStop.setText("Displayed")
            self.testbench.ui.ServiceBrakes.setChecked(False)
            self.testbench.ui.ServiceBrakes.setEnabled(False)
        else:
            self.testbench.ui.PEmergencyStop.setText("Not Displayed")
            self.testbench.ui.ServiceBrakes.setEnabled(True)

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
        time_text = f"{hour_12:02d}:{minute:02d}"

        # Update the QLCDNumber and the AM/PM label
        self.train_ui.Clock_12.display(time_text)
        self.train_ui.AM_PM.setText(am_pm)

    def to_float(self, val_str, default=0.0):
        """Helper for string->float conversion."""
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
    train_model_app.show()
    train_model_app.testbench.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
