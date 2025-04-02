# When infrastructure is displayed, show it (station, switches, railway crossings, lights) / May also put trains here

# For each train on the track, display a train icon correlating to each train & include train name label above train icon

# Retrieving switch postions (0 is for lower # connection, 1 is for higher # connection)
# Ex: (5;6) & (5;11) (0 = 6), (1 = 11)

# Retrieving railway crossing state

# Retrieving light states
###############################################################################
# Main Track Model UI Class
###############################################################################

from Track.TrackModel.track_model_backend import TrackModel
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QTableWidgetItem

class TrackModelFrontEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.red_line = TrackModel("Red")
        self.green_line = TrackModel("Green")
        self.outside_temp = 70.0
        self.track_heater_status = False

    # WIP Uploading a Track Layout with Track Builder
    def upload_track_layout_data(self, file_path):
        self.red_line.parse_track_layout_data(file_path)
        self.green_line.parse_track_layout_data(file_path)
        print("Successfully loaded and parsed layout for Red and Green lines.")

    # Changing Temperature
    def change_temperature(self, new_temp):
        try:
            new_temp = float(new_temp)
            self.outside_temp = new_temp
            self.track_heater_status = new_temp <= 36
            print(f"Updated track temperature: {new_temp}°F, Heater {'On' if self.track_heater_status else 'Off'}")
        except ValueError:
            print("Invalid temperature input.")


# Example usage
if __name__ == "__main__":
    track_model = TrackModelFrontEnd()
    track_model.upload_track_layout_data("Track Layout & Vehicle Data vF5.xlsx")
    track_model.change_temperature(35)