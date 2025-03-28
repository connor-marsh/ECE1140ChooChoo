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
from train_model_testbench import TestBenchApp

class TrainModelFrontEnd(QMainWindow):
    def __init__(self, collection):
        super().__init__()

        # Create TrainCollection and let it populate with trains.
        self.train_collection = collection

        # Use the current_train from the collection.
        self.current_train = None
        # self.current_train = self.train_collection.current_train

        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)
        
        # Setup dropdown for selecting a train model.
        if self.train_collection:
            self.setup_train_dropdown()
        
        # # Load the initial train's data and simulation state.
        # self.load_train_data()
        # self.load_sim_state()

        # Initialize physics and clock timers.
        # self.prev_time = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # 10 Hz update

        self.simulated_time = QTime(11, 59, 0)
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000)

        # Configure emergency brake button.
        self.init_failure_buttons()
        self.init_emergency_button()

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
            # if self.current_train.ui_data.get("emergency_brake", False):
            #     self.train_ui.button_emergency.setChecked(True)
            #     self.train_ui.button_emergency.setEnabled(False)
            #     self.testbench.ui.EmergencyStop.setChecked(True)
            #     self.testbench.ui.EmergencyStop.setEnabled(True)
            #     self.testbench.ui.PEmergencyStop.setText("Enabled")
            # else:
            #     self.train_ui.button_emergency.setChecked(False)
            #     self.train_ui.button_emergency.setEnabled(True)
            #     self.testbench.ui.EmergencyStop.setChecked(False)
            #     self.testbench.ui.EmergencyStop.setEnabled(False)
            #     self.testbench.ui.PEmergencyStop.setText("Disabled")

    def update(self): 
        if self.current_train is not None:
            
            # Directly use attributes:
            velocity_mph = self.current_train.actual_velocity * self.current_train.MPS_TO_MPH
            cmd_speed_mph = self.current_train.wayside_speed * self.current_train.MPS_TO_MPH
            try:
                speed_limit = self.current_train.speed_limit
            except AttributeError:
                speed_limit = 0.0
            speed_limit_mph = speed_limit * self.current_train.MPS_TO_MPH
            
            acceleration_fts2 = self.current_train.current_acceleration * 3.281
            commanded_power = self.current_train.commanded_power
            
            self.train_ui.AccValue.display(acceleration_fts2)
            self.train_ui.SpeedValue.display(velocity_mph)
            self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
            self.train_ui.SpeedLimitValue.display(speed_limit_mph)
            self.train_ui.PowerValue.display(commanded_power / 1000.0)

            # For physical properties, assume they are now stored in the (or use defaults)
            try:
                mass_kg = self.current_train.mass_kg
                grade = self.current_train.grade
                passenger_count = self.current_train.passenger_count
                crew_count = self.current_train.crew_count
                length_m = self.current_train.length_m
                height_m = self.current_train.height_m
                width_m = self.current_train.width_m
            except AttributeError:
                mass_kg = 37103.86
                grade = 0.0
                passenger_count = 0.0
                crew_count = 2.0
                length_m = 32.2
                height_m = 3.42
                width_m = 2.65

            mass_lbs = mass_kg * self.current_train.KG_TO_LBS
            self.train_ui.MassVehicleValue.display(mass_lbs)
            self.train_ui.PassengerCountValue.display(passenger_count)
            self.train_ui.CrewCountValue.display(crew_count)
            self.train_ui.LengthVehicleValue.display(length_m * self.current_train.M_TO_FT)
            self.train_ui.HeightValue.display(height_m * self.current_train.M_TO_FT)
            self.train_ui.WidthValue.display(width_m * self.current_train.M_TO_FT)

            # Announcements from:
            announcements = self.current_train.announcement
            if hasattr(self.train_ui, "Announcement_2"):
                self.train_ui.Announcement_2.setText(announcements)
                self.train_ui.Announcement_2.setStyleSheet("font-size: 20px; font-weight: bold;")

            if hasattr(self.train_ui, "Temperature"):
                display_temp = self.current_train.cabin_temp * 9 / 5 + 32
                self.train_ui.Temperature.setText(f"{display_temp:.2f} °F")
                self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

            if hasattr(self.train_ui, "GradePercentage"):
                self.train_ui.GradePercentageValue.display(grade)
                
            # Color features for auxiliary functions still rely on TestBench UI state.
            self.update_color(self.current_train.service_brakes,
                            self.train_ui.ServiceBrakesOn,
                            self.train_ui.ServiceBrakesOff)
            self.update_color(self.current_train.headlights,
                            self.train_ui.ExteriorLightsOn,
                            self.train_ui.ExteriorLightsOff)
            self.update_color(self.current_train.cabin_lights,
                            self.train_ui.InteriorLightsOn,
                            self.train_ui.InteriorLightsOff)
            self.update_color(self.current_train.left_doors,
                            self.train_ui.LeftDoorOpen,
                            self.train_ui.LeftDoorClosed)
            self.update_color(self.current_train.right_doors,
                            self.train_ui.RightDoorOpen,
                            self.train_ui.RightDoorClosed)

            # self.testbench.update_status()

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

        # se the testbench's on_failure_group_toggled method.
        self.failure_group1.buttonClicked.connect(lambda btn: self.testbench.on_failure_group_toggled("BrakeFailure", btn))
        self.failure_group2.buttonClicked.connect(lambda btn: self.testbench.on_failure_group_toggled("SignalFailure", btn))
        self.failure_group3.buttonClicked.connect(lambda btn: self.testbench.on_failure_group_toggled("EngineFailure", btn))

    def init_emergency_button(self):
        self.train_ui.button_emergency.setCheckable(True)
        # Use a lambda that calls testbench.handle_emergency_button only if self.testbench exists.
        self.train_ui.button_emergency.toggled.connect(
            lambda pressed: self.testbench.handle_emergency_button(pressed)
            if hasattr(self, 'testbench') else None
        )

    # def on_failure_group_toggled(self, failure_type, button):
    #     new_status = button.text()
    #     if failure_type == "BrakeFailure":
    #         self.testbench.ui.BrakeFailure.setText(new_status)
    #     elif failure_type == "SignalFailure":
    #         self.testbench.ui.SignalFailure.setText(new_status)
    #     elif failure_type == "EngineFailure":
    #         self.testbench.ui.EngineFailure.setText(new_status)

    # def handle_emergency_button(self, pressed: bool):
    #     if not self.train_ui.button_emergency.isEnabled():
    #         return
    #     if pressed:
    #         self.train_ui.button_emergency.setEnabled(False)
    #         self.testbench.ui.PEmergencyStop.setText("Enabled")
    #         self.testbench.ui.ServiceBrakes.setChecked(False)
    #         self.testbench.ui.ServiceBrakes.setEnabled(False)
    #         self.testbench.ui.EmergencyStop.setEnabled(True)
    #         self.testbench.ui.EmergencyStop.setChecked(True)
    #         self.testbench.ui.TrainDriver.setChecked(True)
    #         self.testbench.ui.TrainDriver.setEnabled(False)
    #     else:
    #         self.testbench.ui.PEmergencyStop.setText("Disabled")
    #         self.testbench.ui.ServiceBrakes.setEnabled(True)

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
    
    train_model_frontend = TrainModelFrontEnd(None)
    collection = TrainCollection(num_trains=3, model=train_model_frontend)
    train_model_frontend.train_collection = collection
    train_model_frontend.setup_train_dropdown()
    train_model_frontend.current_train = collection.train_list[0]
    train_model_frontend.show()
    
    train_model_testbench = TestBenchApp(collection)    
    train_model_testbench.show()
    
    # link testbench to frontend for communication of values and button presses
    train_model_frontend.testbench = train_model_testbench
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
