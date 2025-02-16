import sys
import os

from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtCore import QTimer

# Import Train Model UI
from TrainModel_UI_Iteration_1 import Ui_MainWindow as TrainModelUI

# Import the updated TestBench UI
from TrainModel_UI_TestBench_Iteration_1 import Ui_TestMainWindow as TestBenchUI

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

##########################################################################
# DATA CLASSES
##########################################################################
class WaysideInputs:
    """
    Holds wayside and commanded data such as speed, authority, commanded power,
    speed limit, and beacon data.
    """
    def __init__(self, speed=0.0, authority=0.0, commanded_power=0.0,
                 speed_limit=0.0, beacon_data=""):
        self.speed = speed
        self.authority = authority
        self.commanded_power = commanded_power
        self.speed_limit = speed_limit
        self.beacon_data = beacon_data

    @staticmethod
    def from_ui(ui, to_float_func):
        """
        Reads wayside-related fields from the TestBench UI and returns a WaysideInputs object.
        """
        return WaysideInputs(
            speed          = to_float_func(ui.WaysideSpeed.text(), 0.0),
            authority      = to_float_func(ui.WaysideAuthority.text(), 0.0),
            commanded_power= to_float_func(ui.CommandedPower.text(), 0.0),
            speed_limit    = to_float_func(ui.SpeedLimit.text(), 0.0),
            beacon_data    = ui.BeaconData.text()
        )

class LightsDoorsData:
    """
    Holds booleans for exterior lights, interior lights, left/right doors, and
    the announcements text.
    """
    def __init__(self, ext_lights=False, int_lights=False,
                 left_doors=False, right_doors=False, service_brakes=False,
                 announcements=""):
        self.service_brakes = service_brakes
        self.ext_lights = ext_lights
        self.int_lights = int_lights
        self.left_doors = left_doors
        self.right_doors = right_doors
        self.announcements = announcements

    @staticmethod
    def from_ui(ui):
        """
        Reads lights, doors, and announcements from the TestBench UI and returns a LightsDoorsData object.
        """
        return LightsDoorsData(
            service_brakes = ui.ServiceBrakes.isChecked(),
            ext_lights   = ui.ExtLights.isChecked(),
            int_lights   = ui.IntLights.isChecked(),
            left_doors   = ui.LeftDoors.isChecked(),
            right_doors  = ui.RightDoors.isChecked(),
            announcements= ui.Announcements.text()
        )

class TrainPhysicalAttributes:
    """
    Holds numeric data for length, height, width, grade, mass, passenger count, crew count.
    """
    def __init__(self, length=0.0, height=0.0, width=0.0,
                 grade=0.0, mass=0.0, passenger_count=0.0,
                 crew_count=0.0):
        self.length = length
        self.height = height
        self.width = width
        self.grade = grade
        self.mass = mass
        self.passenger_count = passenger_count
        self.crew_count = crew_count

    @staticmethod
    def from_ui(ui, to_float_func):
        """
        Reads train physical attribute fields from the TestBench UI and returns a TrainPhysicalAttributes object.
        """
        return TrainPhysicalAttributes(
            length          = to_float_func(ui.LengthVehicle.text(), 0.0),
            height          = to_float_func(ui.HeightVehicle.text(), 0.0),
            width           = to_float_func(ui.WidthVehicle.text(), 0.0),
            grade           = to_float_func(ui.GradePercent.text(), 0.0),
            mass            = to_float_func(ui.MassVehicle.text(), 0.0),
            passenger_count = to_float_func(ui.PassengerCount.text(), 0.0),
            crew_count      = to_float_func(ui.CrewCount.text(), 0.0)
        )

##########################################################################
# TESTBENCH APP
##########################################################################
class TestBenchApp(QMainWindow):
    """
    The UI for your TestBench, feeding data into the Train Model UI.
    """
    def __init__(self, train_app):
        super().__init__()
        self.ui = TestBenchUI()
        self.ui.setupUi(self)
        self.train_app = train_app

    def read_inputs(self):
        """
        Reads user inputs from the TestBench UI and returns
        (wayside_data, lights_doors_data, train_physical_data).
        """
        f = self.train_app.to_float  # Shortcut to the float conversion method in TrainModelApp

        wayside_data        = WaysideInputs.from_ui(self.ui, f)
        lights_doors_data   = LightsDoorsData.from_ui(self.ui)
        train_physical_data = TrainPhysicalAttributes.from_ui(self.ui, f)

        return wayside_data, lights_doors_data, train_physical_data

    def update_status(self):
        """
        Checks if the Train Model UI is displaying correct values,
        updates 'Displayed?' or 'Not Displayed' labels accordingly.
        """
        wayside_speed_str = self.ui.WaysideSpeed.text()
        wayside_speed     = self.train_app.to_float(wayside_speed_str, -999)
        model_speed       = self.train_app.train_ui.CommandedSpeedValue.value()

        if abs(wayside_speed - model_speed) < 0.0001:
            self.ui.WaysideSpeed_2.setText("Displayed")
        else:
            self.ui.WaysideSpeed_2.setText("Not Displayed")

        # Repeat checks for other data (authority, commanded power, lights, etc.) as needed.

##########################################################################
# TRAIN MODEL APP
##########################################################################
class TrainModelApp(QMainWindow):
    """
    The main application that holds the Train Model UI and links to the TestBenchApp.
    """
    def __init__(self):
        super().__init__()
        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)

        self.testbench = TestBenchApp(self)

        # Timer to periodically sync data from the TestBench
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_from_testbench)
        self.timer.start(1000)  # e.g., update every 1 second

        # Make the emergency brake button checkable
        self.train_ui.button_emergency.setCheckable(True)

        # Make the 6 buttons checkable and connect to toggled signals
        self.init_failure_buttons()

        # Connect the toggled signal, rather than clicked
        self.train_ui.button_emergency.toggled.connect(self.mark_emergency_displayed)

    def init_failure_buttons(self):
        # Make the 6 buttons checkable
        self.train_ui.Enabled1.setCheckable(True)
        self.train_ui.Enabled2.setCheckable(True)
        self.train_ui.Enabled3.setCheckable(True)
        self.train_ui.Disabled1.setCheckable(True)
        self.train_ui.Disabled2.setCheckable(True)
        self.train_ui.Disabled3.setCheckable(True)

        # Connect toggled signals
        self.train_ui.Enabled1.toggled.connect(lambda checked: self.on_failure_toggled("Enabled1", checked))
        self.train_ui.Enabled2.toggled.connect(lambda checked: self.on_failure_toggled("Enabled2", checked))
        self.train_ui.Enabled3.toggled.connect(lambda checked: self.on_failure_toggled("Enabled3", checked))
        self.train_ui.Disabled1.toggled.connect(lambda checked: self.on_failure_toggled("Disabled1", checked))
        self.train_ui.Disabled2.toggled.connect(lambda checked: self.on_failure_toggled("Disabled2", checked))
        self.train_ui.Disabled3.toggled.connect(lambda checked: self.on_failure_toggled("Disabled3", checked))

    def on_failure_toggled(self, button_name, checked):
        """
        Called when any of the 'Enabled*'/'Disabled*' buttons is toggled in the Train Model UI.
        We update the corresponding button text in the TestBench UI to 'Displayed' or 'Not Displayed'.
        """
        text_to_set = "Displayed" if checked else "Not Displayed"

        if button_name == "Enabled1":
            self.testbench.ui.BrakeFailure.setText(text_to_set)
        elif button_name == "Disabled1":
            self.testbench.ui.BrakeFailure.setText(text_to_set)

        elif button_name == "Enabled2":
            self.testbench.ui.SignalFailure.setText(text_to_set)
        elif button_name == "Disabled2":
            self.testbench.ui.SignalFailure.setText(text_to_set)

        elif button_name == "Enabled3":
            self.testbench.ui.EngineFailure.setText(text_to_set)
        elif button_name == "Disabled3":
            self.testbench.ui.EngineFailure.setText(text_to_set)

    def update_from_testbench(self):
        """
        Periodically reads data from the TestBench input fields, updates the Train Model UI,
        and lets the TestBench check if the data is displayed.
        """
        wayside_data, lights_doors_data, train_physical_data = self.testbench.read_inputs()

        # Update numeric QLCDNumber fields
        self.train_ui.CommandedSpeedValue.display(wayside_data.speed)
        self.train_ui.SpeedLimitValue.display(wayside_data.speed_limit)
        self.train_ui.PowerValue.display(wayside_data.commanded_power)

        # For demonstration, we do not calculate AccValue here
        # (If your actual code needs acceleration, compute it properly)
        self.train_ui.AccValue.display(wayside_data.authority)

        self.train_ui.LengthVehicleValue.display(train_physical_data.length)
        self.train_ui.HeightValue.display(train_physical_data.height)
        self.train_ui.WidthValue.display(train_physical_data.width)
        self.train_ui.MassVehicleValue.display(train_physical_data.mass)
        self.train_ui.PassengerCountValue.display(train_physical_data.passenger_count)
        self.train_ui.CrewCountValue.display(train_physical_data.crew_count)

        # Toggle background color for Lights, Doors, and Brakes
        if lights_doors_data.service_brakes:
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: #ECEC76; color: black;")
        else:
            self.train_ui.ServiceBrakesOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ServiceBrakesOff.setStyleSheet("background-color: #ECEC76; color: black;")
        
        if lights_doors_data.ext_lights:
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: green; color: white;")
        else:
            self.train_ui.ExteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.ExteriorLightsOff.setStyleSheet("background-color: red; color: white;")

        if lights_doors_data.int_lights:
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: green; color: white;")
        else:
            self.train_ui.InteriorLightsOn.setStyleSheet("background-color: none; color: black;")
            self.train_ui.InteriorLightsOff.setStyleSheet("background-color: red; color: white;")

        if lights_doors_data.left_doors:
            self.train_ui.LeftDoorClosed.setStyleSheet("background-color: none; color: black;")
            self.train_ui.LeftDoorOpen.setStyleSheet("background-color: #ECEC76; color: black;")
        else:
            self.train_ui.LeftDoorOpen.setStyleSheet("background-color: none; color: black;")
            self.train_ui.LeftDoorClosed.setStyleSheet("background-color: #ECEC76; color: black;")

        if lights_doors_data.right_doors:
            self.train_ui.RightDoorClosed.setStyleSheet("background-color: none; color: black;")
            self.train_ui.RightDoorOpen.setStyleSheet("background-color: #ECEC76; color: black;")
        else:
            self.train_ui.RightDoorOpen.setStyleSheet("background-color: none; color: black;")
            self.train_ui.RightDoorClosed.setStyleSheet("background-color: #ECEC76; color: black;")

        # Let the testbench confirm whether or not these values are "Displayed."
        self.testbench.update_status()

    def mark_emergency_displayed(self, pressed: bool):
        """
        If the emergency brake button is toggled on in the Train Model UI,
        mark that on the testbench as 'Displayed'.
        If toggled off, mark 'Not Displayed'.
        """
        if pressed:
            self.testbench.ui.PEmergencyStop.setText("Displayed")
        else:
            self.testbench.ui.PEmergencyStop.setText("Not Displayed")

    def to_float(self, val_str, default=0.0):
        """
        Helper method for safe string->float conversion.
        """
        try:
            return float(val_str)
        except ValueError:
            return default

##########################################################################
# MAIN ENTRY POINT
##########################################################################
def main():
    app = QApplication(sys.argv)
    train_model_app = TrainModelApp()
    train_model_app.show()
    train_model_app.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
