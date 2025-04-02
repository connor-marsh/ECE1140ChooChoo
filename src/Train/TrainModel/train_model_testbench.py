"""
Author: Iyan Nekib
Date: 03-20-2025
Description:

"""

# testbench.py
from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from Train.TrainModel.train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI
from Train.TrainModel.train_model_backend import TrainModel

class TrainModelTestbench(QMainWindow):
    def __init__(self, train_collection, train_integrated=False):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_collection = train_collection
        self.train_integrated = train_integrated

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
            track_data, lights_data, physical_data = self.read_inputs()
            
            # Force the emergency flag to True if the backend is already in emergency state.
            if self.train_collection.train_model_ui.current_train.emergency_brake:
                physical_data["emergency_brake"] = True
            else:
                physical_data["emergency_brake"] = self.ui.EmergencyStop.isChecked()
            
            # Merge dictionaries.
            merged_data = {}
            merged_data.update(track_data)
            if not self.train_integrated:
                merged_data.update(lights_data)
                merged_data.update(physical_data)
            
            # Update the backend with the merged data.
            # if self.train_integrated:
            #     self.train_collection.train_model_ui.current_train.backend.set_input_data(track_data=merged_data)
            # else:
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
            # Clear the backend emergency flag.
            self.train_collection.train_model_ui.current_train.emergency_brake = False
            # Re-enable the frontend emergency button.
            self.train_collection.train_model_ui.train_ui.button_emergency.setEnabled(True)
            self.train_collection.train_model_ui.train_ui.button_emergency.setChecked(False)
            
            # Update testbench UI.
            self.ui.PEmergencyStop.setText("Disabled")
            self.ui.EmergencyStop.setEnabled(False)
            self.ui.EmergencyStop.setChecked(False)
            self.ui.TrainDriver.setEnabled(True)
            self.ui.TrainDriver.setChecked(False)

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
            "beacon_data": self.ui.BeaconData.text(),
            "grade": to_float(self.ui.GradePercent.text(), 0.0),
            "passenger_count": to_float(self.ui.PassengerCount.text(), 0.0),
            "crew_count": to_float(self.ui.CrewCount.text(), 2.0)
        }
        
        lights = {
            "interior_lights": self.ui.IntLights.isChecked(),
            "headlights": self.ui.ExtLights.isChecked(),
            "left_doors": self.ui.LeftDoors.isChecked(),
            "right_doors": self.ui.RightDoors.isChecked(),
            "heating_signal": self.ui.HeatingSignal.isChecked(),
            "air_conditioning_signal": self.ui.ACSignal.isChecked(),
            "announcements": self.ui.Announcements.text() if hasattr(self.ui, "Announcements") else ""
        }

        physical = {
            "commanded_power": to_float(self.ui.CommandedPower.text(), 0.0),
            "service_brake": self.ui.ServiceBrakes.isChecked(),
            "emergency_brake": self.ui.EmergencyStop.isChecked(),
            "actual_speed": to_float(self.ui.ActualVelocity.text(), 0.0),
            "mass_kg": to_float(self.ui.MassVehicle.text(), 37103.86),
            "length_m": to_float(self.ui.LengthVehicle.text(), 32.2),
            "height_m": to_float(self.ui.HeightVehicle.text(), 3.42),
            "width_m": to_float(self.ui.WidthVehicle.text(), 2.65)
        }
        return wayside, lights, physical

    def update_status(self):
        # Retrieve the backend TrainModel from the frontend.
        backend = self.train_collection.train_model_ui.current_train

        # Update failure status labels based on the backend flags.
        self.ui.BrakeFailure.setText("Enabled" if backend.brake_failure else "Disabled")
        self.ui.SignalFailure.setText("Enabled" if backend.signal_failure else "Disabled")
        self.ui.EngineFailure.setText("Enabled" if backend.engine_failure else "Disabled")

        # Update the emergency brake UI elements based on the backend flag.
        if backend.emergency_brake:
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

        # Update additional UI elements (existing logic from your code):
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

        internal_mph = backend.actual_speed * backend.MPS_TO_MPH
        speed_ui = self.train_collection.train_model_ui.train_ui.SpeedValue.value()
        if abs(internal_mph - speed_ui) < 0.0001:
            self.ui.ActualVelocity.setText(f"{internal_mph:.2f}")
        else:
            self.ui.ActualVelocity.setText("Not Displayed")

        self.ui.Temperature.setText(self.train_collection.train_model_ui.train_ui.Temperature.text())