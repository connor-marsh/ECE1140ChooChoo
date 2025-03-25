from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from train_model_ui_testbench_iteration_1 import Ui_TestMainWindow as TestBenchUI
from train_model_backend import TrainModel

class TestBenchApp(QMainWindow):
    def __init__(self, train_model):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_model = train_model

        self.ui.PEmergencyStop.setText("Disabled")
        self.ui.BrakeFailure.setText("Disabled")
        self.ui.SignalFailure.setText("Disabled")
        self.ui.EngineFailure.setText("Disabled")

        self.ui.EmergencyStop.setCheckable(True)
        self.ui.EmergencyStop.setEnabled(False)
        self.ui.EmergencyStop.setChecked(False)
        self.ui.EmergencyStop.toggled.connect(self.handle_emergency_release)
        self.ui.TrainDriver.toggled.connect(self.handle_train_driver)

    def update_train_model(self):
        # Sample code
        data = {}
        data["wayside_speed"] = 0
        self.train_model.update_from_testbench(data)


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
        f = TrainModelFrontEnd.to_float
        wayside = TrainModelFrontEnd.read_wayside_data(self.ui, f)
        lights = TrainModelFrontEnd.read_lights_doors_data(self.ui)
        physical = TrainModelFrontEnd.read_train_physical_data(self.ui, f)
        return wayside, lights, physical

    def update_status(self):
        f = TrainModelFrontEnd.to_float
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