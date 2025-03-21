# frontend.py
import sys
import os
import math

# Add the parent directory (if needed)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
from train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI
from train_collection import TrainCollection
from train_model_backend import TrainSimulator

class TrainModelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)

        # Create simulation backend instance.
        self.simulator = TrainSimulator()

        # Create TrainCollection and populate with trains.
        self.train_collection = TrainCollection()
        for _ in range(3):
            self.train_collection.createTrain()
        self.current_train = self.train_collection.train_list[0] if self.train_collection.train_list else None

        # Setup dropdown for selecting a train model.
        self.setup_train_dropdown()

        # Create the testbench window.
        self.testbench = TestBenchApp(self)

        # Initialize physics and clock timers.
        self.prev_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_from_testbench)
        self.timer.start(100)  # 10 Hz update

        self.simulated_time = QTime(11, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # Configure emergency brake button.
        self.train_ui.button_emergency.setCheckable(True)
        self.init_failure_buttons()
        self.train_ui.button_emergency.toggled.connect(self.handle_emergency_button)

    def setup_train_dropdown(self):
        """Embeds a small dropdown in the menuTrain_ID_1 menu."""
        self.train_dropdown = QComboBox()
        self.train_dropdown.setFixedSize(120, 25)
        for idx, train in enumerate(self.train_collection.train_list):
            self.train_dropdown.addItem(getattr(train, "name", f"Train ID {idx+1}"))
        self.train_dropdown.currentIndexChanged.connect(self.on_train_selection_changed)
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(self.train_dropdown)
        self.train_ui.menuTrain_ID_1.addAction(widget_action)

    def on_train_selection_changed(self, index):
        if 0 <= index < len(self.train_collection.train_list):
            self.current_train = self.train_collection.train_list[index]
            self.train_ui.menuTrain_ID_1.setTitle(f"Train ID {index+1}")
            if hasattr(self.train_ui, "currentTrainLabel"):
                self.train_ui.currentTrainLabel.setText(f"Selected: {self.train_dropdown.currentText()}")

    @staticmethod
    def read_wayside_data(ui, to_float_func):
        commanded_power = to_float_func(ui.CommandedPower.text(), 0.0)
        if commanded_power > 120000:
            commanded_power = 120000.0
        elif commanded_power < 0:
            commanded_power = 0.0
        return {
            "commanded_speed": to_float_func(ui.WaysideSpeed.text(), 0.0),
            "authority": to_float_func(ui.WaysideAuthority.text(), 0.0),
            "commanded_power": commanded_power,
            "speed_limit": to_float_func(ui.SpeedLimit.text(), 0.0),
            "beacon_data": ui.BeaconData.text(),
        }

    @staticmethod
    def read_lights_doors_data(ui):
        return {
            "service_brakes": ui.ServiceBrakes.isChecked(),
            "ext_lights": ui.ExtLights.isChecked(),
            "int_lights": ui.IntLights.isChecked(),
            "left_doors": ui.LeftDoors.isChecked(),
            "right_doors": ui.RightDoors.isChecked(),
            "announcements": ui.Announcements.text(),
            "ac_signal": ui.ACSignal.isChecked(),
            "heat_signal": ui.HeatingSignal.isChecked()
        }

    @staticmethod
    def read_train_physical_data(ui, to_float_func):
        base_mass_kg = to_float_func(ui.MassVehicle.text(), 37103.86)
        passenger_count = to_float_func(ui.PassengerCount.text(), 0.0)
        crew_count = to_float_func(ui.CrewCount.text(), 2.0)
        added_passenger_mass = passenger_count * 70.0
        added_crew_mass = crew_count * 70.0
        length_m = to_float_func(ui.LengthVehicle.text(), 32.2)
        height_m = to_float_func(ui.HeightVehicle.text(), 3.42)
        width_m = to_float_func(ui.WidthVehicle.text(), 2.65)
        grade_percent = to_float_func(ui.GradePercent.text(), 0.0)
        temperature = to_float_func(ui.Temperature.text(), 25.0)
        
        if grade_percent > 60:
            grade_percent = 60.0
        elif grade_percent < 0:
            grade_percent = 0.0
        return {
            "length_m": length_m,
            "height_m": height_m,
            "width_m": width_m,
            "grade": grade_percent,
            "mass_kg": base_mass_kg + added_passenger_mass + added_crew_mass,
            "passenger_count": passenger_count,
            "crew_count": crew_count,
            "temperature": temperature
        }

    def update_from_testbench(self):
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0
        self.prev_time = current_time

        wayside_data, lights_data, train_data = self.testbench.read_inputs()
        updated = self.simulator.update(
            dt, wayside_data, lights_data, train_data,
            emergency_active=self.train_ui.button_emergency.isChecked()
        )
        self.simulator.current_acceleration = updated["acceleration"]
        self.simulator.actual_velocity = updated["velocity"]

        velocity_mph = self.simulator.actual_velocity * self.simulator.MPS_TO_MPH
        cmd_speed_mph = wayside_data["commanded_speed"] * self.simulator.MPS_TO_MPH
        speed_limit_mph = wayside_data["speed_limit"] * self.simulator.MPS_TO_MPH
        acceleration_fts2 = self.simulator.current_acceleration * 3.281

        self.train_ui.AccValue.display(acceleration_fts2)
        self.train_ui.SpeedValue.display(velocity_mph)
        self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
        self.train_ui.SpeedLimitValue.display(speed_limit_mph)
        self.train_ui.PowerValue.display(wayside_data["commanded_power"] / 1000.0)

        mass_lbs = train_data["mass_kg"] * self.simulator.KG_TO_LBS
        self.train_ui.MassVehicleValue.display(mass_lbs)
        self.train_ui.PassengerCountValue.display(train_data["passenger_count"])
        self.train_ui.CrewCountValue.display(train_data["crew_count"])
        self.train_ui.LengthVehicleValue.display(train_data["length_m"] * self.simulator.M_TO_FT)
        self.train_ui.HeightValue.display(train_data["height_m"] * self.simulator.M_TO_FT)
        self.train_ui.WidthValue.display(train_data["width_m"] * self.simulator.M_TO_FT)

        if hasattr(self.train_ui, "Announcement_2"):
            announcements = lights_data["announcements"]
            self.train_ui.Announcement_2.setText(announcements)
            self.train_ui.Announcement_2.setStyleSheet("font-size: 20px; font-weight: bold;")

        if hasattr(self.train_ui, "Temperature"):
            display_temp = (updated["cabin_temp"])
            self.train_ui.Temperature.setText(f"{display_temp:.2f} °F")
            self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

        if hasattr(self.train_ui, "GradePercentage"):
            self.train_ui.GradePercentageValue.display(train_data["grade"])

        self.testbench.update_status()

    def init_failure_buttons(self):
        self.train_ui.Enabled1.setCheckable(True)
        self.train_ui.Disabled1.setCheckable(True)
        self.train_ui.Enabled2.setCheckable(True)
        self.train_ui.Disabled2.setCheckable(True)
        self.train_ui.Enabled3.setCheckable(True)
        self.train_ui.Disabled3.setCheckable(True)

        self.failure_group1 = QButtonGroup(self)
        self.failure_group1.setExclusive(True)
        self.failure_group1.addButton(self.train_ui.Enabled1)
        self.failure_group1.addButton(self.train_ui.Disabled1)

        self.failure_group2 = QButtonGroup(self)
        self.failure_group2.setExclusive(True)
        self.failure_group2.addButton(self.train_ui.Enabled2)
        self.failure_group2.addButton(self.train_ui.Disabled2)

        self.failure_group3 = QButtonGroup(self)
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
        hour_12 = hour % 12 or 12
        time_text = f"{hour_12:02d}:{minute:02d}"
        self.train_ui.Clock_12.display(time_text)
        self.train_ui.AM_PM.setText(am_pm)

    @staticmethod
    def to_float(val_str, default=0.0):
        try:
            return float(val_str)
        except ValueError:
            return default

class TestBenchApp(QMainWindow):
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
        f = TrainModelApp.to_float
        wayside = TrainModelApp.read_wayside_data(self.ui, f)
        lights = TrainModelApp.read_lights_doors_data(self.ui)
        physical = TrainModelApp.read_train_physical_data(self.ui, f)
        return wayside, lights, physical

    def update_status(self):
        f = TrainModelApp.to_float
        cmd_speed = self.ui.WaysideSpeed.text()
        cmd_val = f(cmd_speed, -999)
        cmd_val_mph = cmd_val * self.train_app.simulator.MPS_TO_MPH
        model_val = self.train_app.train_ui.CommandedSpeedValue.value()
        if abs(cmd_val_mph - model_val) < 0.0001:
            self.ui.WaysideSpeed_2.setText(f"{cmd_val_mph:.2f}")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")
        auth_str = self.ui.WaysideAuthority.text()
        auth_val = f(auth_str, 0.0)
        if abs(auth_val) > 0.0001:
            self.ui.WaysideAuthority_2.setText(f"{(auth_val * 3.281):.2f}")
        else:
            self.ui.WaysideAuthority_2.setText("Not Displayed")
        speed_str = self.ui.SpeedLimit.text()
        speed_val = f(speed_str, 0.0)
        speed_val_mph = speed_val * self.train_app.simulator.MPS_TO_MPH
        model_speed_limit = self.train_app.train_ui.SpeedLimitValue.value()
        if abs(speed_val_mph - model_speed_limit) < 0.0001:
            self.ui.SpeedLimit_2.setText(f"{speed_val_mph:.2f}")
        else:
            self.ui.SpeedLimit_2.setText("Not Displayed")
        speed_ui = self.train_app.train_ui.SpeedValue.value()
        internal_mph = self.train_app.simulator.actual_velocity * self.train_app.simulator.MPS_TO_MPH
        if abs(internal_mph - speed_ui) < 0.0001:
            self.ui.ActualVelocity.setText(f"{internal_mph:.2f}")
        else:
            self.ui.ActualVelocity.setText("Not Displayed")
        self.ui.Temperature.setText(self.train_app.train_ui.Temperature.text())

def main():
    app = QApplication(sys.argv)
    window = TrainModelApp()
    window.show()
    window.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
