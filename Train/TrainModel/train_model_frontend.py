# frontend.py
import sys
import os
import math

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = "1"

# Add the parent directory (if needed)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
from train_model_backend import TrainModel

class TrainModelFrontEnd(QMainWindow):
    def __init__(self, collection):
        super().__init__()
        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)

        # Create TrainCollection and let it populate with trains.
        self.train_collection = collection

        # Use the current_train from the collection.
        self.current_train = None

        # Setup dropdown for selecting a train model.
        self.setup_train_dropdown()

        # Create the testbench window.
        from train_model_testbench import TestBenchApp  # Lazy import to avoid circular dependency
        self.testbench = TestBenchApp(self)
        
        # # Load the initial train's data and simulation state.
        # self.load_train_data()
        # self.load_sim_state()

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
        
    # def save_current_train_data(self):
    #     """Save every numeric value, announcement, and auxiliary function state from the TestBench UI (and emergency brake state) into the current train’s ui_data."""
    #     data = {
    #         "commanded_speed": self.to_float(self.testbench.ui.WaysideSpeed.text(), 0.0),
    #         "authority": self.to_float(self.testbench.ui.WaysideAuthority.text(), 0.0),
    #         "commanded_power": self.to_float(self.testbench.ui.CommandedPower.text(), 0.0),
    #         "speed_limit": self.to_float(self.testbench.ui.SpeedLimit.text(), 0.0),
    #         "beacon_data": self.testbench.ui.BeaconData.text(),
    #         "announcements": self.testbench.ui.Announcements.text() if hasattr(self.testbench.ui, "Announcements") else "",
    #         "grade": self.to_float(self.testbench.ui.GradePercent.text(), 0.0) if hasattr(self.testbench.ui, "GradePercent") else 0.0,
    #         "passenger_count": self.to_float(self.testbench.ui.PassengerCount.text(), 0.0) if hasattr(self.testbench.ui, "PassengerCount") else 0.0,
    #         "service_brakes": self.testbench.ui.ServiceBrakes.isChecked() if hasattr(self.testbench.ui, "ServiceBrakes") else False,
    #         "ext_lights": self.testbench.ui.ExtLights.isChecked() if hasattr(self.testbench.ui, "ExtLights") else False,
    #         "int_lights": self.testbench.ui.IntLights.isChecked() if hasattr(self.testbench.ui, "IntLights") else False,
    #         "left_doors": self.testbench.ui.LeftDoors.isChecked() if hasattr(self.testbench.ui, "LeftDoors") else False,
    #         "right_doors": self.testbench.ui.RightDoors.isChecked() if hasattr(self.testbench.ui, "RightDoors") else False,
    #         "ac_signal": self.testbench.ui.ACSignal.isChecked() if hasattr(self.testbench.ui, "ACSignal") else False,
    #         "heat_signal": self.testbench.ui.HeatingSignal.isChecked() if hasattr(self.testbench.ui, "HeatingSignal") else False,
    #         "emergency_brake": self.train_ui.button_emergency.isChecked() if hasattr(self.train_ui, "button_emergency") else False,
    #     }
    #     if self.current_train is not None:
    #         self.current_train.ui_data = data

    # def load_train_data(self):
    #     """Load saved values from the current train’s ui_data into the TestBench UI and update emergency brake state."""
    #     if self.current_train is None or not hasattr(self.current_train, "ui_data"):
    #         return
    #     data = self.current_train.ui_data
    #     self.testbench.ui.WaysideSpeed.setText(str(data.get("commanded_speed", 0.0)))
    #     self.testbench.ui.WaysideAuthority.setText(str(data.get("authority", 0.0)))
    #     self.testbench.ui.CommandedPower.setText(str(data.get("commanded_power", 0.0)))
    #     self.testbench.ui.SpeedLimit.setText(str(data.get("speed_limit", 0.0)))
    #     self.testbench.ui.BeaconData.setText(data.get("beacon_data", ""))
    #     if hasattr(self.testbench.ui, "Announcements"):
    #         self.testbench.ui.Announcements.setText(data.get("announcements", ""))
    #     if hasattr(self.testbench.ui, "GradePercent"):
    #         self.testbench.ui.GradePercent.setText(str(data.get("grade", 0.0)))
    #     if hasattr(self.testbench.ui, "PassengerCount"):
    #         self.testbench.ui.PassengerCount.setText(str(data.get("passenger_count", 0.0)))
    #     if hasattr(self.testbench.ui, "ServiceBrakes"):
    #         self.testbench.ui.ServiceBrakes.setChecked(data.get("service_brakes", False))
    #     if hasattr(self.testbench.ui, "ExtLights"):
    #         self.testbench.ui.ExtLights.setChecked(data.get("ext_lights", False))
    #     if hasattr(self.testbench.ui, "IntLights"):
    #         self.testbench.ui.IntLights.setChecked(data.get("int_lights", False))
    #     if hasattr(self.testbench.ui, "LeftDoors"):
    #         self.testbench.ui.LeftDoors.setChecked(data.get("left_doors", False))
    #     if hasattr(self.testbench.ui, "RightDoors"):
    #         self.testbench.ui.RightDoors.setChecked(data.get("right_doors", False))
    #     if hasattr(self.testbench.ui, "ACSignal"):
    #         self.testbench.ui.ACSignal.setChecked(data.get("ac_signal", False))
    #     if hasattr(self.testbench.ui, "HeatingSignal"):
    #         self.testbench.ui.HeatingSignal.setChecked(data.get("heat_signal", False))
    #     if hasattr(self.train_ui, "button_emergency"):
    #         self.train_ui.button_emergency.setChecked(data.get("emergency_brake", False))

    # def save_current_sim_state(self):
    #     """Save current simulation state from the simulator into the current train’s sim_state."""
    #     if self.current_train is not None:
    #         self.current_train.sim_state = {
    #             "actual_velocity": self.current_train.backend.actual_velocity,
    #             "current_acceleration": self.current_train.backend.current_acceleration,
    #             "previous_acceleration": self.current_train.backend.previous_acceleration,
    #             "cabin_temp": self.current_train.backend.cabin_temp
    #         }

    # def load_sim_state(self):
    #     """Load simulation state from the current train’s sim_state into the simulator."""
    #     if self.current_train is None or not hasattr(self.current_train, "sim_state"):
    #         return
    #     state = self.current_train.sim_state
    #     self.current_train.backend.actual_velocity = state.get("actual_velocity", 0.0)
    #     self.current_train.backend.current_acceleration = state.get("current_acceleration", 0.0)
    #     self.current_train.backend.previous_acceleration = state.get("previous_acceleration", 0.0)
    #     self.current_train.backend.cabin_temp = state.get("cabin_temp", 25.0)

    def on_train_selection_changed(self, index):
        # Save current train's UI and simulation state before switching.
        # self.save_current_train_data()
        # self.save_current_sim_state()
        if 0 <= index < len(self.train_collection.train_list):
            self.current_train = self.train_collection.train_list[index]
            self.train_ui.menuTrain_ID_1.setTitle(f"Train ID {index+1}")
            if hasattr(self.train_ui, "currentTrainLabel"):
                self.train_ui.currentTrainLabel.setText(f"Selected: {self.train_dropdown.currentText()}")
            # Load new train's data and simulation state.
            # self.load_train_data()
            # self.load_sim_state()
            # Update emergency brake state.
            if self.current_train.ui_data.get("emergency_brake", False):
                self.train_ui.button_emergency.setChecked(True)
                self.train_ui.button_emergency.setEnabled(False)
                self.testbench.ui.EmergencyStop.setChecked(True)
                self.testbench.ui.EmergencyStop.setEnabled(True)
                self.testbench.ui.PEmergencyStop.setText("Enabled")
            else:
                self.train_ui.button_emergency.setChecked(False)
                self.train_ui.button_emergency.setEnabled(True)
                self.testbench.ui.EmergencyStop.setChecked(False)
                self.testbench.ui.EmergencyStop.setEnabled(False)
                self.testbench.ui.PEmergencyStop.setText("Disabled")

    # @staticmethod
    # def read_wayside_data(ui, to_float_func):
    #     commanded_power = to_float_func(ui.CommandedPower.text(), 0.0)
    #     if commanded_power > 120000:
    #         commanded_power = 120000.0
    #     elif commanded_power < 0:
    #         commanded_power = 0.0
    #     return {
    #         "commanded_speed": to_float_func(ui.WaysideSpeed.text(), 0.0),
    #         "authority": to_float_func(ui.WaysideAuthority.text(), 0.0),
    #         "commanded_power": commanded_power,
    #         "speed_limit": to_float_func(ui.SpeedLimit.text(), 0.0),
    #         "beacon_data": ui.BeaconData.text(),
    #     }

    # @staticmethod
    # def read_lights_doors_data(ui):
    #     return {
    #         "service_brakes": ui.ServiceBrakes.isChecked(),
    #         "ext_lights": ui.ExtLights.isChecked(),
    #         "int_lights": ui.IntLights.isChecked(),
    #         "left_doors": ui.LeftDoors.isChecked(),
    #         "right_doors": ui.RightDoors.isChecked(),
    #         "announcements": ui.Announcements.text(),
    #         "ac_signal": ui.ACSignal.isChecked(),
    #         "heat_signal": ui.HeatingSignal.isChecked()
    #     }

    # @staticmethod
    # def read_train_physical_data(ui, to_float_func):
    #     base_mass_kg = to_float_func(ui.MassVehicle.text(), 37103.86)
    #     passenger_count = to_float_func(ui.PassengerCount.text(), 0.0)
    #     crew_count = to_float_func(ui.CrewCount.text(), 2.0)
    #     added_passenger_mass = passenger_count * 70.0
    #     added_crew_mass = crew_count * 70.0
    #     length_m = to_float_func(ui.LengthVehicle.text(), 32.2)
    #     height_m = to_float_func(ui.HeightVehicle.text(), 3.42)
    #     width_m = to_float_func(ui.WidthVehicle.text(), 2.65)
    #     grade_percent = to_float_func(ui.GradePercent.text(), 0.0)
    #     temperature = to_float_func(ui.Temperature.text(), 25.0)
        
    #     if grade_percent > 60:
    #         grade_percent = 60.0
    #     elif grade_percent < 0:
    #         grade_percent = 0.0
    #     return {
    #         "length_m": length_m,
    #         "height_m": height_m,
    #         "width_m": width_m,
    #         "grade": grade_percent,
    #         "mass_kg": base_mass_kg + added_passenger_mass + added_crew_mass,
    #         "passenger_count": passenger_count,
    #         "crew_count": crew_count,
    #         "temperature": temperature
    #     }

    def update(self):
        current_time = QDateTime.currentMSecsSinceEpoch()
        if self.prev_time is None:
            self.prev_time = current_time
            return
        dt = (current_time - self.prev_time) / 1000.0
        self.prev_time = current_time

        # # Step 1: Let the testbench do the merging into backend
        # self.testbench.update_train_model()

        # # Step 2: Now do the physics
        # updated = self.current_train.backend.update(dt)

        # Step 3: Extract sub-values from the merged ui_data
        #    (Because the testbench + update_from_testbench merged them)
        # ui_data = self.current_train.backend.ui_data
        # wayside_data = {
        #     "commanded_speed": self.current_train.backend.commanded_speed,
        #     "commanded_power": ui_data.get("commanded_power", 0.0),
        #     "speed_limit": ui_data.get("speed_limit", 0.0),
        #     "beacon_data": ui_data.get("beacon_data", ""),
        # }
        # lights_data = {
        #     "announcements": ui_data.get("announcements", ""),
        #     "service_brakes": ui_data.get("service_brakes", False),
        #     "ext_lights": ui_data.get("ext_lights", False),
        #     "int_lights": ui_data.get("int_lights", False),
        #     "left_doors": ui_data.get("left_doors", False),
        #     "right_doors": ui_data.get("right_doors", False),
        # }
        # train_data = {
        #     "mass_kg": ui_data.get("mass_kg", 0.0),
        #     "grade": ui_data.get("grade", 0.0),
        #     "passenger_count": ui_data.get("passenger_count", 0.0),
        #     "crew_count": ui_data.get("crew_count", 0.0),
        #     "length_m": ui_data.get("length_m", 0.0),
        #     "height_m": ui_data.get("height_m", 0.0),
        #     "width_m": ui_data.get("width_m", 0.0),
        # }

        # Step 4: Use 'updated' plus these sub-dicts to update the front-end UI
        # updated = self.current_train.backend.update(dt)
        self.current_train.backend.current_acceleration = updated["current_acceleration"]
        self.current_train.backend.actual_velocity = updated["velocity"]

        velocity_mph = self.current_train.backend.actual_velocity * self.current_train.backend.MPS_TO_MPH
        cmd_speed_mph = wayside_data["commanded_speed"] * self.current_train.backend.MPS_TO_MPH
        speed_limit_mph = wayside_data["speed_limit"] * self.current_train.backend.MPS_TO_MPH
        acceleration_fts2 = self.current_train.backend.current_acceleration * 3.281

        self.train_ui.AccValue.display(acceleration_fts2)
        self.train_ui.SpeedValue.display(velocity_mph)
        self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
        self.train_ui.SpeedLimitValue.display(speed_limit_mph)
        self.train_ui.PowerValue.display(wayside_data["commanded_power"] / 1000.0)

        mass_lbs = train_data["mass_kg"] * self.current_train.backend.KG_TO_LBS
        self.train_ui.MassVehicleValue.display(mass_lbs)
        self.train_ui.PassengerCountValue.display(train_data["passenger_count"])
        self.train_ui.CrewCountValue.display(train_data["crew_count"])
        self.train_ui.LengthVehicleValue.display(train_data["length_m"] * self.current_train.backend.M_TO_FT)
        self.train_ui.HeightValue.display(train_data["height_m"] * self.current_train.backend.M_TO_FT)
        self.train_ui.WidthValue.display(train_data["width_m"] * self.current_train.backend.M_TO_FT)

        if hasattr(self.train_ui, "Announcement_2"):
            announcements = lights_data["announcements"]
            self.train_ui.Announcement_2.setText(announcements)
            self.train_ui.Announcement_2.setStyleSheet("font-size: 20px; font-weight: bold;")

        if hasattr(self.train_ui, "Temperature"):
            display_temp = updated["cabin_temp"]
            self.train_ui.Temperature.setText(f"{display_temp:.2f} °F")
            self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

        if hasattr(self.train_ui, "GradePercentage"):
            self.train_ui.GradePercentageValue.display(train_data["grade"])
            
        # color features for auxiliary functions based on TestBench UI state.
        self.update_color(self.testbench.ui.ServiceBrakes.isChecked(),
                          self.train_ui.ServiceBrakesOn,
                          self.train_ui.ServiceBrakesOff)
        self.update_color(self.testbench.ui.ExtLights.isChecked(),
                          self.train_ui.ExteriorLightsOn,
                          self.train_ui.ExteriorLightsOff)
        self.update_color(self.testbench.ui.IntLights.isChecked(),
                          self.train_ui.InteriorLightsOn,
                          self.train_ui.InteriorLightsOff)
        self.update_color(self.testbench.ui.LeftDoors.isChecked(),
                          self.train_ui.LeftDoorOpen,
                          self.train_ui.LeftDoorClosed)
        self.update_color(self.testbench.ui.RightDoors.isChecked(),
                          self.train_ui.RightDoorOpen,
                          self.train_ui.RightDoorClosed)

        self.testbench.update_status()

    @staticmethod
    def update_color(checked, widget_on, widget_off):
        """Set style sheets based on a boolean condition.
        
        If checked is True, the "on" widget gets yellow and the "off" widget gets default;
        otherwise, the "on" widget gets default and the "off" widget gets yellow.
        """
        if checked:
            widget_off.setStyleSheet("background-color: none; color: black;")
            widget_on.setStyleSheet("background-color: yellow; color: black;")
        else:
            widget_on.setStyleSheet("background-color: none; color: black;")
            widget_off.setStyleSheet("background-color: yellow; color: black;")

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

def main():
    app = QApplication(sys.argv)
    from train_collection import TrainCollection
    window=TrainModelFrontEnd(TrainCollection())
    window.show()
    window.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
