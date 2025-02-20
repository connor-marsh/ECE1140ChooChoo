import sys
import os
import random  # Import random for generating ticket sales value.
import pandas as pd
from track_model_enums import Occupancy, Failures
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem

# Import the UI files generated from Qt Designer
from track_model_ui import Ui_MainWindow as TrackModelUI
from test_bench_track_model import Ui_MainWindow as TBTrackModelUI

# Ensure proper scaling on high-DPI screens
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

###############################################################################
# TEST BENCH APP
###############################################################################

# Initializes the Test Bench App and connects UI elements to their handlers.
class TestBenchApp(QMainWindow):
    def __init__(self, track_model):
        super(TestBenchApp, self).__init__()
        self.ui = TBTrackModelUI()  # Load the Test Bench UI
        self.ui.setupUi(self)
        self.track_model = track_model  # Reference to the main TrackModelApp

        # Connect Test Bench controls to update backend values.
        self.ui.track_temperature_input_tb.editingFinished.connect(self.update_track_temperature)
        self.ui.set_passenger_count_input_tb.editingFinished.connect(self.update_passenger_count)
        self.ui.set_departing_input_tb.editingFinished.connect(self.update_departing_count)
        self.ui.select_block_occupancy_input_tb.currentIndexChanged.connect(self.update_block_occupancy)
        self.ui.toggle_switch_input_tb.clicked.connect(self.toggle_track_switch)
        self.ui.railway_crossing_toggle_input_tb.clicked.connect(self.toggle_railway_crossing)
        self.ui.select_station_tb.currentIndexChanged.connect(self.update_traffic_signal)
        
        # NOTE: We have removed any Test Bench connection for updating boarding side.
        # Update beacon data when Test Bench block selection changes.
        self.ui.track_line_selected_tb.currentIndexChanged.connect(self.update_beacon_data)
        self.ui.block_section_selected_tb.currentIndexChanged.connect(self.update_beacon_data)
        self.ui.block_number_selected_tb.currentIndexChanged.connect(self.update_beacon_data)

    # Returns the selected block key from Test Bench UI (for updating the currently selected block).
    def get_selected_block_key(self):
        line = self.ui.track_line_selected_tb.currentText().replace(" Line", "").strip()
        section = self.ui.block_section_selected_tb.currentText().strip()
        block_number = self.ui.block_number_selected_tb.currentText().strip()
        try:
            block_number = int(block_number)
            return (line, section, block_number)
        except ValueError:
            return None

    # Updates beacon data based on the selected block in the Test Bench UI.
    def update_beacon_data(self):
        block_key = self.get_selected_block_key()
        if block_key is None or block_key not in self.track_model.block_data:
            self.ui.beacon_data_output_tb.setText("")
            return
        block = self.track_model.block_data[block_key]
        if "Transponder" in block["infrastructure"]:
            beacon_text = f"This is block {block_key[1]}{block_key[2]}"
            self.ui.beacon_data_output_tb.setText(beacon_text)
            print(f"Beacon Data updated: {beacon_text}")
        else:
            self.ui.beacon_data_output_tb.setText("")

    # Updates occupancy for the block selected in Test Bench UI.
    def update_block_occupancy(self):
        occupancy = self.ui.select_block_occupancy_input_tb.currentText()
        block_key = self.get_selected_block_key()
        if block_key not in self.track_model.block_data:
            print(f"Block {block_key} not found in Test Bench Update!")
            return
        self.track_model.block_data[block_key]["occupancy"] = occupancy
        print(f"Updated Occupancy to {occupancy} for Block {block_key} via Test Bench")
        self.track_model.populate_table()
        self.track_model.update_ui()

    # Updates the traffic signal for the block selected in Test Bench UI.
    def update_traffic_signal(self):
        signal = self.ui.select_station_tb.currentText()
        block_key = self.get_selected_block_key()
        if block_key not in self.track_model.block_data:
            print(f"Block {block_key} not found for traffic signal update!")
            return
        block = self.track_model.block_data[block_key]
        if "Light" in block["infrastructure"]:
            self.track_model.block_data[block_key]["traffic_signal"] = signal
            print(f"Traffic signal updated to {signal} for Block {block_key}")
            self.track_model.populate_table()
            self.track_model.update_ui()
        else:
            print("Selected block does not have lights.")

    # Updates track temperature from the Test Bench input.
    def update_track_temperature(self):
        temp_text = self.ui.track_temperature_input_tb.text()
        try:
            temp = float(temp_text)
            self.track_model.track_temperature = temp
            self.track_model.update_track_heater_status()
            self.track_model.populate_table()
            self.track_model.update_ui()
        except ValueError:
            print("Invalid track temperature value.")

    # Updates passenger count from the Test Bench input.
    def update_passenger_count(self):
        count_text = self.ui.set_passenger_count_input_tb.text()
        try:
            count = int(count_text)
            self.track_model.passenger_count = count
            self.track_model.update_train_data_table()
        except ValueError:
            print("Invalid passenger count.")

    # Updates departing count display in the Track Model UI based on Test Bench input.
    def update_departing_count(self):
        departing_text = self.ui.set_departing_input_tb.text()
        try:
            departing = int(departing_text)
            self.track_model.track_model_ui.departing_count_value.setText(str(departing))
        except ValueError:
            print("Invalid departing count.")

    # Toggles the switch state for the selected block in Test Bench UI.
    def toggle_track_switch(self):
        block_key = self.get_selected_block_key()
        if block_key is None:
            print("Invalid block selection for switch toggle.")
            return
        block = self.track_model.block_data.get(block_key)
        if block is None:
            print(f"Block {block_key} not found for switch toggle.")
            return
        infrastructure = block.get("infrastructure", "").strip()
        if infrastructure.startswith("SWITCH"):
            current_state = block.get("switch_state", False)
            new_state = not current_state
            self.track_model.block_data[block_key]["switch_state"] = new_state
            try:
                inner = infrastructure.split("(", 1)[1].rstrip(")")
                options = inner.split(";")
                option1 = options[0].strip().replace("-", "->")
                option2 = options[1].strip().replace("-", "->")
            except Exception as e:
                print("Error parsing switch infrastructure:", e)
                option1 = "5->6"
                option2 = "5->11"
            output_text = option2 if new_state else option1
            self.ui.track_switch_output_value_tb.setText(output_text)
            print(f"Switch toggled for Block {block_key}: {output_text}")
            self.track_model.populate_table()
            self.track_model.update_ui()
        else:
            print("Selected block does not support switch toggling.")

    # Toggles the railway crossing signal for the selected block in Test Bench UI.
    def toggle_railway_crossing(self):
        block_key = self.get_selected_block_key()
        if block_key is None:
            print("Invalid block selection for railway crossing toggle.")
            return
        block = self.track_model.block_data.get(block_key)
        if block is None:
            print(f"Block {block_key} not found for railway crossing toggle.")
            return
        if block.get("infrastructure", "").strip() == "RAILWAY CROSSING":
            current_state = block.get("railway_signal", False)
            new_state = not current_state
            self.track_model.block_data[block_key]["railway_signal"] = new_state
            print(f"Railway crossing toggled for Block {block_key}: {'Active' if new_state else 'Inactive'}")
            self.track_model.populate_table()
            self.track_model.update_ui()
        else:
            print("Selected block does not have a railway crossing.")

###############################################################################
# TRACK MODEL APP
###############################################################################

# Initializes the Track Model App and connects UI elements to their handlers.
class TrackModelApp(QMainWindow):
    def __init__(self):
        super(TrackModelApp, self).__init__()
        self.track_model_ui = TrackModelUI()  # Load the Track Model UI
        self.track_model_ui.setupUi(self)

        # Initialize Data
        self.block_data = {}          # Dictionary to store track data for each block
        self.track_temperature = 25   # Default track temperature
        self.passenger_count = 0      # Default passenger count
        self.station_mapping = {}     # Mapping from station name to its station side
        self.ticket_sales = 0         # Variable for ticket sales (equal to boarding count)

        # Connect import button
        self.track_model_ui.import_track_layout_button.clicked.connect(self.input_file)

        # Connect failure toggles (for block failures)
        self.track_model_ui.track_circuit_failure_toggle.clicked.connect(lambda: self.update_block_failures("Track Circuit Failure"))
        self.track_model_ui.broken_rail_failure_toggle.clicked.connect(lambda: self.update_block_failures("Broken Rail Failure"))
        self.track_model_ui.power_failure_toggle.clicked.connect(lambda: self.update_block_failures("Power Failure"))
        self.track_model_ui.reset_errors_button.clicked.connect(self.reset_failures)

        # Connect ComboBoxes (in the Track Model UI) to update display
        self.track_model_ui.track_line_selected.currentIndexChanged.connect(self.update_ui)
        self.track_model_ui.block_section_selected.currentIndexChanged.connect(self.update_ui)
        self.track_model_ui.block_number_selected.currentIndexChanged.connect(self.update_ui)
        # Connect the select_station combobox to update boarding side exclusively.
        self.track_model_ui.select_station.currentIndexChanged.connect(self.update_boarding_side)

        # Timer for temperature stepping (optional)
        self.temp_timer = QtCore.QTimer(self)
        self.temp_timer.timeout.connect(self.step_temperature_up)
        self.temp_timer.start(5000)

    # Loads Excel data into the block_data dictionary and builds station mapping.
    def input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Track Layout File", "", "Excel Files (*.xlsx);;All Files (*)")
        if file_path:
            df = pd.read_excel(file_path)
            print("File loaded:", file_path)
            for _, row in df.iterrows():
                block_key = (row["Line"], row["Section"], row["Block Number"])
                infrastructure = row["Infrastructure"] if pd.notna(row["Infrastructure"]) else ""
                station_side = row["Station Side"] if "Station Side" in row and pd.notna(row["Station Side"]) else "None"
                self.block_data[block_key] = {
                    "block_length": row["Block Length"],
                    "speed_limit": row["Speed Limit"],
                    "infrastructure": infrastructure,
                    "elevation": row["Elevation"],
                    "cumulative_elevation": row["Cumulative Elevation"],
                    "occupancy": Occupancy.UNOCCUPIED.value,
                    "failures": Failures.NONE.value,
                    "switch_state": False,
                    "railway_signal": False,
                    "traffic_signal": "None",
                    "station_side": station_side
                }
                # Build station mapping if this row represents a station.
                if "STATION;" in infrastructure:
                    parts = infrastructure.split(";", 1)
                    if len(parts) > 1:
                        station_name = parts[1].strip()
                        self.station_mapping[station_name] = station_side
            self.populate_table()
            self.update_ui()
            # Update boarding side and ticket sales based on default select_station value.
            self.update_boarding_side()

    # Updates the boarding side display based solely on the station selected in the select_station combobox.
    def update_boarding_side(self):
        selected_station = self.track_model_ui.select_station.currentText().strip()
        if not selected_station:
            self.track_model_ui.boarding_side_value.setText("None")
            print("No station selected in select_station combobox.")
            return

        if selected_station in self.station_mapping:
            station_side = self.station_mapping[selected_station]
            self.track_model_ui.boarding_side_value.setText(station_side)
            print(f"Updated boarding side for station {selected_station}: {station_side}")
        else:
            self.track_model_ui.boarding_side_value.setText("None")
            print(f"No boarding side found for station {selected_station}.")
        # Generate and update ticket sales (equal to boarding count) after updating boarding side.
        self.update_ticket_sales()

    # Generates a random value between 1 and 70 for ticket sales (equal to boarding count)
    # and updates the boarding_count_value and ticket_sales_value UI elements.
    def update_ticket_sales(self):
        self.ticket_sales = random.randint(1, 70)
        self.track_model_ui.boarding_count_value.setText(str(self.ticket_sales))
        self.track_model_ui.ticket_sales_value.setText(str(self.ticket_sales))
        print(f"Updated ticket sales (boarding count): {self.ticket_sales}")

    # Updates the track heater display based on the current track temperature.
    def update_track_heater_status(self):
        heater_status = "On" if self.track_temperature <= 36 else "Off"
        if hasattr(self.track_model_ui, "track_heater_value"):
            self.track_model_ui.track_heater_value.setText(heater_status)
        print(f"Track heater updated: {heater_status}")

    # Updates the failure status of the currently selected block from the Track Model UI.
    def update_block_failures(self, failure_type):
        block_key = self.get_selected_block_key()
        if block_key in self.block_data:
            self.block_data[block_key]["failures"] = failure_type
            self.populate_table()
            self.update_ui()

    # Resets the failure status of the currently selected block.
    def reset_failures(self):
        block_key = self.get_selected_block_key()
        if block_key in self.block_data:
            self.block_data[block_key]["failures"] = Failures.NONE.value
            print(f"Failures reset for Block {block_key}")
            self.populate_table()
            self.update_ui()

    # Populates the track table with updated block data.
    def populate_table(self):
        table = self.track_model_ui.track_table_display
        table.setRowCount(len(self.block_data))
        for row_idx, (block_key, block) in enumerate(self.block_data.items()):
            table.setItem(row_idx, 0, QTableWidgetItem(str(block["occupancy"])))
            table.setItem(row_idx, 1, QTableWidgetItem(str(block["infrastructure"])))
            table.setItem(row_idx, 2, QTableWidgetItem(str(block["failures"])))

    # Updates the block data display based on the selected block in the Test Bench UI.
    def update_ui(self):
        block_key = self.get_selected_test_bench_block_key()
        if block_key not in self.block_data:
            return

        block = self.block_data[block_key]
        self.track_model_ui.block_selected_value.setText(f"{block_key[1]}{block_key[2]}")
        self.track_model_ui.block_length_value.setText(str(block["block_length"]))
        self.track_model_ui.speed_limit_value.setText(str(block["speed_limit"]))
        self.track_model_ui.block_occupied_value.setText(block["occupancy"])
        self.track_model_ui.track_temperature_value.setText(str(self.track_temperature))
        self.update_track_heater_status()

        # Update station data: update station_value if this block is a station.
        if "STATION;" in block["infrastructure"]:
            station_name = block["infrastructure"].replace("STATION; ", "")
            self.track_model_ui.station_value.setText(station_name)
            # Do NOT update boarding_side_value here.
        else:
            self.track_model_ui.station_value.setText("None")

        # Update railway crossing display.
        if block.get("infrastructure", "").strip() == "RAILWAY CROSSING":
            self.track_model_ui.railway_crossing_value.setText("Active" if block.get("railway_signal", False) else "Inactive")
        else:
            self.track_model_ui.railway_crossing_value.setText("None")

        # Update traffic signal display if block has lights.
        if "Light" in block["infrastructure"]:
            self.track_model_ui.traffic_signal_value.setText(block.get("traffic_signal", "None"))
        else:
            self.track_model_ui.traffic_signal_value.setText("None")

    # Updates passenger count in the train data table.
    def update_train_data_table(self):
        table = self.track_model_ui.train_data_table
        if table.rowCount() == 0:
            table.setRowCount(1)
        table.setItem(0, 1, QTableWidgetItem(str(self.passenger_count)))

    # Increments track temperature if it is ≤ 36 and updates the UI.
    def step_temperature_up(self):
        if self.track_temperature <= 36:
            self.track_temperature += 0.5
            self.update_ui()

    # Returns the selected block key from Track Model UI.
    def get_selected_block_key(self):
        line = self.track_model_ui.track_line_selected.currentText().replace(" Line", "").strip()
        section = self.track_model_ui.block_section_selected.currentText().strip()
        block_number = self.track_model_ui.block_number_selected.currentText().strip()
        try:
            block_number = int(block_number)
            return (line, section, block_number)
        except ValueError:
            return None

    # Returns the selected block key from Test Bench UI (for updating the currently selected block).
    def get_selected_test_bench_block_key(self):
        line = self.track_model_ui.track_line_selected.currentText().replace(" Line", "").strip()
        section = self.track_model_ui.block_section_selected.currentText().strip()
        block_number = self.track_model_ui.block_number_selected.currentText().strip()
        try:
            block_number = int(block_number)
            return (line, section, block_number)
        except ValueError:
            return None

###############################################################################
# MAIN
###############################################################################

# Main function to run the application.
def main():
    app = QtWidgets.QApplication(sys.argv)
    track_model_window = TrackModelApp()
    track_model_window.show()
    test_bench_window = TestBenchApp(track_model_window)
    test_bench_window.show()
    sys.exit(app.exec_())

# Run the application if this script is executed.
if __name__ == "__main__":
    main()
