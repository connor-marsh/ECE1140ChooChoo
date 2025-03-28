# testbench.py
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI
from train_model_backend import TrainModel

class TestBenchApp(QMainWindow):
    def __init__(self, train_collection):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_collection = train_collection

        self.ui.PEmergencyStop.setText("Disabled")
        self.ui.BrakeFailure.setText("Disabled")
        self.ui.SignalFailure.setText("Disabled")
        self.ui.EngineFailure.setText("Disabled")

        self.ui.EmergencyStop.setCheckable(True)
        self.ui.EmergencyStop.setEnabled(False)
        self.ui.EmergencyStop.setChecked(False)
        self.ui.EmergencyStop.toggled.connect(self.handle_emergency_release)
        self.ui.TrainDriver.toggled.connect(self.handle_train_driver)
        
        # Initialize timer for periodic update.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_train_model)
        self.timer.start(100)  # 10 Hz update rate

    def update_train_model(self):
        # Get the currently selected train from the front end.
        self.current_train = self.train_collection.train_model_ui.current_train
        if self.current_train:
            # Read inputs from the testbench UI.
            wayside_data, lights_data, physical_data = self.read_inputs()
            
            # Merge dictionaries.
            merged_data = {}
            merged_data.update(wayside_data)
            merged_data.update(lights_data)
            merged_data.update(physical_data)
            
            # Include the emergency flag.
            merged_data["emergency_active"] = self.ui.EmergencyStop.isChecked()
            
            # Update the backend with the merged data.
            self.train_collection.train_model_ui.current_train.backend.set_input_data(testbench_data=merged_data)
        
        # Update the testbench display status.
        self.update_status()

    def handle_train_driver(self, checked: bool):
        if checked:
            self.train_collection.train_model_ui.train_ui.button_emergency.setChecked(True)
            self.train_collection.train_model_ui.train_ui.button_emergency.setEnabled(False)
            self.ui.PEmergencyStop.setText("Enabled")
            self.ui.EmergencyStop.setEnabled(True)
            self.ui.EmergencyStop.setChecked(True)
            self.ui.TrainDriver.setEnabled(False)
        else:
            self.train_collection.train_model_ui.train_ui.button_emergency.setEnabled(True)
            self.train_collection.train_model_ui.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)

    def handle_emergency_release(self, checked: bool):
        if not checked:
            self.train_collection.train_model_ui.train_ui.button_emergency.setEnabled(True)
            self.train_collection.train_model_ui.train_ui.button_emergency.setChecked(False)
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)
            self.ui.TrainDriver.setEnabled(True)
            self.ui.TrainDriver.setChecked(False)
            
    def on_failure_group_toggled(self, failure_type, button):
        new_status = button.text()
        if failure_type == "BrakeFailure":
            self.ui.BrakeFailure.setText(new_status)
        elif failure_type == "SignalFailure":
            self.ui.SignalFailure.setText(new_status)
        elif failure_type == "EngineFailure":
            self.ui.EngineFailure.setText(new_status)

    # def handle_emergency_button(self, pressed: bool):
    #     if not self.train_ui.button_emergency.isEnabled():
    #         return
    #     if pressed:
    #         self.train_ui.button_emergency.setEnabled(False)
    #         self.ui.PEmergencyStop.setText("Enabled")
    #         self.ui.ServiceBrakes.setChecked(False)
    #         self.ui.ServiceBrakes.setEnabled(False)
    #         self.ui.EmergencyStop.setEnabled(True)
    #         self.ui.EmergencyStop.setChecked(True)
    #         self.ui.TrainDriver.setChecked(True)
    #         self.ui.TrainDriver.setEnabled(False)
    #     else:
    #         self.ui.PEmergencyStop.setText("Disabled")
    #         self.ui.ServiceBrakes.setEnabled(True)
    
    def handle_emergency_button(self, pressed: bool):
        if pressed:
            self.ui.PEmergencyStop.setText("Enabled")
            self.ui.ServiceBrakes.setChecked(False)
            self.ui.ServiceBrakes.setEnabled(False)
            self.ui.EmergencyStop.setEnabled(True)
            self.ui.EmergencyStop.setChecked(True)
            self.ui.TrainDriver.setChecked(True)
            self.ui.TrainDriver.setEnabled(False)
        else:
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.ServiceBrakes.setEnabled(True)


    def read_inputs(self):
        # Helper to convert text to float.
        def to_float(val_str, default=0.0):
            try:
                return float(val_str)
            except ValueError:
                return default

        wayside = {
            "commanded_speed": to_float(self.ui.WaysideSpeed.text(), 0.0),
            "authority": to_float(self.ui.WaysideAuthority.text(), 0.0),
            "beacon_data": self.ui.BeaconData.text()
        }
        
        lights = {
            "int_lights": self.ui.IntLights.isChecked(),
            "ext_lights": self.ui.ExtLights.isChecked(),
            "left_doors": self.ui.LeftDoors.isChecked(),
            "right_doors": self.ui.RightDoors.isChecked(),
            "heat_signal": self.ui.HeatingSignal.isChecked(),
            "ac_signal": self.ui.ACSignal.isChecked(),
            "announcements": self.ui.Announcements.text() if hasattr(self.ui, "Announcements") else ""
        }

        physical = {
            "commanded_power": to_float(self.ui.CommandedPower.text(), 0.0),
            "service_brakes": self.ui.ServiceBrakes.isChecked(),
            "emergency_active": self.ui.EmergencyStop.isChecked(),
            "actual_velocity": to_float(self.ui.ActualVelocity.text(), 0.0),
            "grade": to_float(self.ui.GradePercent.text(), 0.0),
            "passenger_count": to_float(self.ui.PassengerCount.text(), 0.0),
            "crew_count": to_float(self.ui.CrewCount.text(), 2.0),
            "mass_kg": to_float(self.ui.MassVehicle.text(), 37103.86),
            "length_m": to_float(self.ui.LengthVehicle.text(), 32.2),
            "height_m": to_float(self.ui.HeightVehicle.text(), 3.42),
            "width_m": to_float(self.ui.WidthVehicle.text(), 2.65),
            "speed_limit": to_float(self.ui.SpeedLimit.text(), 0.0)
        }
        return wayside, lights, physical

    def update_status(self):
        # Update labels in the testbench to reflect the backend values.
        backend = self.train_collection.train_model_ui.current_train

        cmd_val = backend.wayside_speed
        cmd_val_mph = cmd_val * backend.MPS_TO_MPH
        model_val = self.train_collection.train_model_ui.train_ui.CommandedSpeedValue.value()
        if abs(cmd_val_mph - model_val) < 0.0001:
            self.ui.WaysideSpeed_2.setText(f"{cmd_val_mph:.2f}")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")

        auth_val = backend.wayside_authority
        if abs(auth_val) > 0.0001:
            self.ui.WaysideAuthority_2.setText(f"{(auth_val * backend.M_TO_FT):.2f}")
        else:
            self.ui.WaysideAuthority_2.setText("Not Displayed")

        speed_str = self.ui.SpeedLimit.text()
        try:
            speed_val = float(speed_str)
        except ValueError:
            speed_val = 0.0
        speed_val_mph = speed_val * backend.MPS_TO_MPH
        model_speed_limit = self.train_collection.train_model_ui.train_ui.SpeedLimitValue.value()
        if abs(speed_val_mph - model_speed_limit) < 0.0001:
            self.ui.SpeedLimit_2.setText(f"{speed_val_mph:.2f}")
        else:
            self.ui.SpeedLimit_2.setText("Not Displayed")

        internal_mph = backend.actual_velocity * backend.MPS_TO_MPH
        speed_ui = self.train_collection.train_model_ui.train_ui.SpeedValue.value()
        if abs(internal_mph - speed_ui) < 0.0001:
            self.ui.ActualVelocity.setText(f"{internal_mph:.2f}")
        else:
            self.ui.ActualVelocity.setText("Not Displayed")

        self.ui.Temperature.setText(self.train_collection.train_model_ui.train_ui.Temperature.text())
