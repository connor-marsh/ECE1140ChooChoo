"""
Author: Iyan Nekib
Date: 03-20-2025
Description:
"""

# frontend.py
import sys
import os
import random

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = "1"

from PyQt5.QtWidgets import QMainWindow, QApplication, QComboBox, QWidgetAction, QButtonGroup
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from Train.TrainModel.train_model_ui_iteration_1 import Ui_MainWindow as TrainModelUI
from Train.TrainModel.train_model_testbench import TrainModelTestbench
import globals.global_clock as global_clock

class TrainModelFrontEnd(QMainWindow):
    def __init__(self, collection):
        super().__init__()

        # Create TrainCollection and let it populate with trains.
        self.train_collection = collection

        # Use the current_train from the collection.
        self.current_train = None

        self.train_ui = TrainModelUI()
        self.train_ui.setupUi(self)
        
        # UI state dictionary to hold frontend-specific failure states and announcements (keyed by train id in dropdown)
        # Keys: Failure states, Announcement
        self.ui_states = {}
        
        # Setup dropdown for selecting a train model.
        self.setup_train_dropdown()

        # Initialize physics timers.
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)  # 10 Hz update

        self.global_clock = global_clock.clock

        # Configure emergency brake and failure buttons.
        self.init_failure_buttons()
        self.init_emergency_button()

        # Rotating advertisements:
        self.setup_advertisements()

    def setup_advertisements(self):
        """Initializes advertisement rotation using the UI's advertisement labels."""
        self.ad_paths = [
            r"src\Train\TrainModel\Assets\pizza_hut_ad_1.jpg",
            r"src\Train\TrainModel\Assets\McD.jpg",
            r"src\Train\TrainModel\Assets\whopper.jpg"
        ]
        self.ad_labels = [
            self.train_ui.Advertisements,
            self.train_ui.Advertisements_2,
            self.train_ui.Advertisements_3
        ]
        
        self.ad_timer = QTimer(self)
        self.ad_timer.timeout.connect(self.rotate_advertisements)
        self.ad_timer.start(5000)  # 5 seconds

        self.rotate_advertisements()

    def rotate_advertisements(self):
        """Randomly assign different advertisement images to each ad label."""
        selected_ads = (
            random.sample(self.ad_paths, len(self.ad_labels))
            if len(self.ad_paths) >= len(self.ad_labels)
            else [random.choice(self.ad_paths) for _ in range(len(self.ad_labels))]
        )
        for label, ad_path in zip(self.ad_labels, selected_ads):
            label.setPixmap(QPixmap(ad_path))

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
            if self.current_train is None:
                self.current_train = self.train_collection.train_list[0]
                # Load UI state for the first train.
                self.load_ui_state(self.current_train)

    def get_ui_state(self, train):
        """Returns the UI state dict for a given train. Initialize if not present.
        Only the failure states and announcements are stored.
        """
        key = id(train)
        if key not in self.ui_states:
            # Defaults: all failure states disabled and empty announcement.
            self.ui_states[key] = {
                'BrakeFailure': False,
                'SignalFailure': False,
                'EngineFailure': False,
                'announcement': ""
            }
        return self.ui_states[key]

    def save_current_ui_state(self):
        """Saves the current UI failure states and announcement for the active train and propagates failure states to the backend."""
        if self.current_train is not None:
            state = self.get_ui_state(self.current_train)
            state['BrakeFailure'] = self.train_ui.Enabled1.isChecked()
            state['SignalFailure'] = self.train_ui.Enabled2.isChecked()
            state['EngineFailure'] = self.train_ui.Enabled3.isChecked()
            if hasattr(self.train_ui, "Announcement_2"):
                state['announcement'] = self.train_ui.Announcement_2.text()
            
            # Propagate failure states to backend:
            self.current_train.brake_failure = state['BrakeFailure']
            self.current_train.signal_failure = state['SignalFailure']
            self.current_train.engine_failure = state['EngineFailure']

    def load_ui_state(self, train):
        """Loads the UI failure state and announcement for the given train, updates UI elements and propagates to backend."""
        state = self.get_ui_state(train)
        if state['BrakeFailure']:
            self.train_ui.Enabled1.setChecked(True)
        else:
            self.train_ui.Disabled1.setChecked(True)
        self.current_train.brake_failure = state['BrakeFailure']
        
        if state['SignalFailure']:
            self.train_ui.Enabled2.setChecked(True)
        else:
            self.train_ui.Disabled2.setChecked(True)
        self.current_train.signal_failure = state['SignalFailure']
        
        if state['EngineFailure']:
            self.train_ui.Enabled3.setChecked(True)
        else:
            self.train_ui.Disabled3.setChecked(True)
        self.current_train.engine_failure = state['EngineFailure']
        
        if hasattr(self.train_ui, "Announcement_2"):
            self.train_ui.Announcement_2.setText(state.get('announcement', ""))

    def on_train_selection_changed(self, index):
        # Save current UI state before switching trains.
        if self.current_train is not None:
            self.save_current_ui_state()
        if 0 <= index < len(self.train_collection.train_list):
            self.current_train = self.train_collection.train_list[index]
            self.train_ui.menuTrain_ID_1.setTitle(f"Train ID {index+1}")
            if hasattr(self.train_ui, "currentTrainLabel"):
                self.train_ui.currentTrainLabel.setText(f"Selected: {self.train_dropdown.currentText()}")
            # Load the stored UI state for the new train and propagate to backend.
            self.load_ui_state(self.current_train)

    def update(self): 
        self.train_ui.Clock_12.display(self.global_clock.text)
        self.train_ui.AM_PM.setText(self.global_clock.am_pm)
        
        if self.current_train is not None:
            # Dynamic values from backend.
            velocity_mph = self.current_train.actual_speed * self.current_train.MPS_TO_MPH
            cmd_speed_mph = self.current_train.wayside_speed * self.current_train.MPS_TO_MPH
            wayside_authority_yd = self.current_train.wayside_authority * self.current_train.M_TO_YARD
            
            acceleration_fts2 = self.current_train.current_acceleration * 3.281
            commanded_power = self.current_train.commanded_power
            
            self.train_ui.AccValue.display(acceleration_fts2)
            self.train_ui.SpeedValue.display(velocity_mph)
            self.train_ui.CommandedSpeedValue.display(cmd_speed_mph)
            self.train_ui.SpeedLimitValue.display(wayside_authority_yd)
            self.train_ui.PowerValue.display(commanded_power / 1000.0)

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
            
            # The emergency brake is updated directly from the backend.
            self.train_ui.button_emergency.setEnabled(not self.current_train.emergency_brake)
            self.train_ui.button_emergency.setChecked(self.current_train.emergency_brake)
            
            # Leave emergency and failure states alone; their propagation happens in the handlers.
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
                
            # Update colors for auxiliary features.
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
        """Set styles based on a boolean condition."""
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

        # Default to "Disabled"
        self.train_ui.Disabled1.setChecked(True)
        self.train_ui.Disabled2.setChecked(True)
        self.train_ui.Disabled3.setChecked(True)

        # Connect toggles to update both UI state and backend.
        self.failure_group1.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("BrakeFailure", btn))
        self.failure_group2.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("SignalFailure", btn))
        self.failure_group3.buttonClicked.connect(lambda btn: self.on_failure_group_toggled("EngineFailure", btn))

    def init_emergency_button(self):
        self.train_ui.button_emergency.setCheckable(True)
        self.train_ui.button_emergency.clicked.connect(self.handle_emergency_button)

    def on_failure_group_toggled(self, failure_type, button):
        new_status = (button.text() == "Enabled")
        state = self.get_ui_state(self.current_train)
        state[failure_type] = new_status

        if failure_type == "BrakeFailure":
            self.current_train.brake_failure = new_status
        elif failure_type == "SignalFailure":
            self.current_train.signal_failure = new_status
        elif failure_type == "EngineFailure":
            self.current_train.engine_failure = new_status

    def handle_emergency_button(self, pressed: bool):
        # Propagate emergency brake directly to the backend.
        new_state = self.train_ui.button_emergency.isChecked()
        self.current_train.emergency_brake = new_state
        if new_state:
            self.current_train.send_emergency_brake_signal = True

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
    train_model_frontend.load_ui_state(train_model_frontend.current_train)
    train_model_frontend.show()
    
    train_model_testbench = TrainModelTestbench(collection)    
    train_model_testbench.show()    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
