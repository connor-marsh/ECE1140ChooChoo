# frontend.py
import sys
import os

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = "1"

# Add the parent directory (if needed)
current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, QDateTime, QTime, Qt
from train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
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
        self.setup_train_dropdown()

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
        self.train_dropdown.currentIndexChanged.connect(self.on_train_selection_changed)
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(self.train_dropdown)
        self.train_ui.menuTrain_ID_1.addAction(widget_action)

    def update_train_dropdown(self):
        if self.train_collection:
            self.train_dropdown.clear()
            for idx, train in enumerate(self.train_collection.train_list):
                self.train_dropdown.addItem(getattr(train, "name", f"Train ID {idx+1}"))
            # If we initialize a connection with 0 trains, this makes it so that the first train created automatically gets selected
            # As opposed to needing to select it manually after its created, which would be gross
            if self.current_train==None:
                self.current_train=self.train_collection.train_list[0]

    def on_train_selection_changed(self, index):
        if 0 <= index < len(self.train_collection.train_list):
            self.current_train = self.train_collection.train_list[index]
            self.train_ui.menuTrain_ID_1.setTitle(f"Train ID {index+1}")
            if hasattr(self.train_ui, "currentTrainLabel"):
                self.train_ui.currentTrainLabel.setText(f"Selected: {self.train_dropdown.currentText()}")        

    def update(self): 
        if self.current_train is not None:
            
            # Directly use attributes:
            velocity_mph = self.current_train.actual_speed * self.current_train.MPS_TO_MPH
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
                display_temp = self.current_train.actual_temperature * 9 / 5 + 32
                self.train_ui.Temperature.setText(f"{display_temp:.2f} °F")
                self.train_ui.Temperature.setAlignment(Qt.AlignCenter)

            if hasattr(self.train_ui, "GradePercentage"):
                self.train_ui.GradePercentageValue.display(grade)
                
            # Color features for auxiliary functions still rely on TestBench UI state.
            self.update_color(self.current_train.service_brake,
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

        # set the on_failure_group_toggled method.
        self.failure_group1.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("BrakeFailure", btn))
        self.failure_group2.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("SignalFailure", btn))
        self.failure_group3.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("EngineFailure", btn))

    def init_emergency_button(self):
        self.train_ui.button_emergency.setCheckable(True)
        self.train_ui.button_emergency.toggled.connect(self.handle_emergency_button)

    def on_failure_group_toggled(self, failure_type, button):
        new_status = button.text() 
        if failure_type == "BrakeFailure":
            self.current_train.brake_failure = (new_status == "Enabled")
        elif failure_type == "SignalFailure":
            self.current_train.signal_failure = (new_status == "Enabled")
        elif failure_type == "EngineFailure":
            self.current_train.engine_failure = (new_status == "Enabled")

    def handle_emergency_button(self, pressed: bool):
        # Only act on the rising edge (when pressed becomes True).
        if pressed:
            self.current_train.driver_emergency_brake = True
            # Disable the frontend emergency button so it stays pressed.
            self.train_ui.button_emergency.setEnabled(False)

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
    train_model_frontend.update_train_dropdown()
    train_model_frontend.current_train = collection.train_list[0]
    train_model_frontend.show()
    
    train_model_testbench = TestBenchApp(collection)    
    train_model_testbench.show()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
