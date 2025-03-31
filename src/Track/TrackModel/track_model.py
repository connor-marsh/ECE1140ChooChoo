import sys
import os
import random
import pandas as pd
from track_model_enums import Occupancy, Failures
from globals.track_data_class import TrackDataClass
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem

# Import the UI files generated from Qt Designer
from track_model_ui import Ui_MainWindow as TrackModelUI
from test_bench_track_model import Ui_MainWindow as TBTrackModelUI

# Ensure proper scaling on high-DPI screens
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

###############################################################################
# Track Model Testbench
###############################################################################

# Wayside Module

    # Send commanded speed & authority

    # Initialize a train

# Train Module

    # Select a train to simulate

    # Send specific train loc update

    # Receive commanded speed & authority

    # Receive track data

# CTC

    # Receive ticket sales

###############################################################################
# Block Class
###############################################################################

class Block:
    def __init__(self, block_id, length, grade, speed_limit, elevation, cumulative_elevation, infrastructure, station_side):
        self.block_id = block_id
        self.length = length
        self.grade = grade
        self.speed_limit = speed_limit
        self.elevation = elevation
        self.cumulative_elevation = cumulative_elevation
        self.infrastructure = infrastructure
        self.station_side = station_side
        self.occupancy = Occupancy.UNOCCUPIED
        self.failures = Failures.NONE
        self.switch_state = False
        self.railway_signal = False
        self.traffic_signal = "None"
        self.beacon_data = None

###############################################################################
# Track BackEnd
###############################################################################

class TrackBackend:
    def __init__(self, name):
        self.name = name
        self.block_data = {}

    # Parsing data sent from main track file
        def parse_track_layout_data(self, filepath):
            """
            Loads and parses track layout using the TrackDataClass.
            """
            self.track_data = TrackDataClass(filepath)
            print(f"[{self.name}] Loaded layout for {self.track_data.line_name} line.")
            print(f"  Total Blocks: {len(self.track_data.blocks)}")
            for territory, blocks in self.track_data.territory_counts.items():
                devices = self.track_data.device_counts[territory]
                print(f"  Territory {territory}: {blocks} blocks, {devices['switches']} switches, "
                    f"{devices['lights']} lights, {devices['crossings']} crossings")

    # Updating switch position , should display the proper next block
    # XOR with current position list and compare to see if update
    def update_switch_states_from_wayside(self, switch_updates):
        switch_blocks = [block for block in self.block_data.values() if "SWITCH" in block.infrastructure]

        for i, desired_state in enumerate(switch_updates):
            if i >= len(switch_blocks):
                break  # Safety check

            block = switch_blocks[i]
            if block.switch_state != bool(desired_state):  # XOR behavior
                block.switch_state = bool(desired_state)
                direction = "higher-numbered" if desired_state else "lower-numbered"
                print(f"[Wayside Update] Switch at Block {block.block_id} set to {direction} connection.")

    # Updating railway crossing position, should display if open/closed
    # XOR with current position list and compare to see if update
    def update_railway_crossings_from_wayside(self, crossing_updates):
        crossing_blocks = [block for block in self.block_data.values() if "RAILWAY CROSSING" in block.infrastructure]

        for i, desired_state in enumerate(crossing_updates):
            if i >= len(crossing_blocks):
                break

            block = crossing_blocks[i]
            if block.railway_signal != bool(desired_state):  # XOR behavior
                block.railway_signal = bool(desired_state)
                state = "ACTIVE (train approaching)" if desired_state else "INACTIVE (cars can cross)"
                print(f"[Wayside Update] Railway Crossing at Block {block.block_id} is now {state}.")



    # Updating light states, should display green/red
    # XOR with current position list and compare to see if update
    def update_light_states_from_wayside(self, light_updates):
        light_blocks = [block for block in self.block_data.values() if "Light" in block.infrastructure]

        for i, desired_state in enumerate(light_updates):
            if i >= len(light_blocks):
                break

            block = light_blocks[i]
            current_green = block.traffic_signal == "Green"
            if current_green != bool(desired_state):  # XOR behavior
                block.traffic_signal = "Green" if desired_state else "Red"
                print(f"[Wayside Update] Light at Block {block.block_id} turned {block.traffic_signal}.")



    # Reading wayside values
    def update_from_wayside_outputs(self, switch_list, light_list, crossing_list):
        self.update_switch_states_from_wayside(switch_list)
        self.update_light_states_from_wayside(light_list)
        self.update_railway_crossings_from_wayside(crossing_list)


    # Updating block occupancies, should read if train, maintenance, or failure is there
    # OR with train, maintenance, and failures
    def update_block_occupancy(self, block_key, occupancy_status): # Need to add train func to read changes
        block = self.block_data.get(block_key)
        if block:
            block.occupancy = Occupancy[occupancy_status.upper()]
            print(f"Block {block.block_id} occupancy updated to {block.occupancy.name}")

    # Send beacon data when a train is on the specific block?
    def send_beacon_data(self, block_key): # Need to add train func to read changes
        block = self.block_data.get(block_key)
        if block and "Transponder" in block.infrastructure:
            block.beacon_data = f"This is block {block.block_id[1]}{block.block_id[2]}".encode()
            print(f"Beacon data sent for block {block.block_id}")

    # Sending section data to frontend, can probably scrap
    # Returns a list of block keys that belong to the given section, could scrap if only blocks shown and not section divides
    def send_section_data(self, section_id):
        section_blocks = []

        for block_key in self.block_data:
            # Example: "GreenA1"
            line_len = len(self.name)  # "Red" or "Green"
            section_char = block_key[line_len]  # Should be one letter: 'A', 'B', etc.

            if section_char == section_id:
                section_blocks.append(block_key)

        print(f"[{self.name}] Section '{section_id}' contains blocks: {section_blocks}")
        return section_blocks

    # Sends main block information
    # Returns the Block for the specified block key
    def send_block_data(self, block_id_str):
        block = self.block_data.get(block_id_str)

        if not block:
            print(f"[{self.name}] Block {block_id_str} not found.")
            return None

        return [
            block.block_id,
            block.length,
            block.grade,
            block.speed_limit,
            block.elevation,
            block.cumulative_elevation,
            block.infrastructure,
            block.station_side,
            block.occupancy.name,
            block.failures.name,
            block.switch_state,
            block.railway_signal,
            block.traffic_signal,
            block.beacon_data.decode() if block.beacon_data else None
        ]
    
    # Sending Wayside Commanded Speed and Authority to Train
    # Triple redundancy, so send 3 times
    def send_wayside_commanded(self, train_id, wayside_speed, wayside_authority):
        speed_votes = [wayside_speed for _ in range(3)]
        authority_votes = [wayside_authority for _ in range(3)]

        print(f"[{self.name}] Sending to Train {train_id}:")
        print(f"  Speed Votes: {speed_votes}")
        print(f"  Authority Votes: {authority_votes}")

        train = self.train_registry.get(train_id)
        if train:
            train.receive_commanded_data(speed_votes, authority_votes)
        else:
            print(f"[{self.name}] Train {train_id} not found.")


    # Initializing a train

    # Wayside will send when to initialize a train




###############################################################################
# Track FrontEnd
###############################################################################

# Initializing UI

# When a section is clicked, zoom in (may scrap)
    def load_section(self, section_id, line):
        if line.lower() == "green":
            block_ids = self.backend.green_line.send_section_data(section_id)
        else:
            block_ids = self.backend.red_line.send_section_data(section_id)

# When a block is clicked, display block information
    def load_block(self, block_id, line):
        if line.lower() == "green":
            block_data = self.backend.green_line.send_block_data(block_id)
        else:
            block_data = self.backend.red_line.send_block_data(block_id)

# When infrastructure is displayed, show it (station, switches, railway crossings, lights) / May also put trains here

# For each train on the track, display a train icon correlating to each train & include train name label above train icon

# Retrieving switch postions (0 is for lower # connection, 1 is for higher # connection)
# Ex: (5;6) & (5;11) (0 = 6), (1 = 11)

# Retrieving railway crossing state

# Retrieving light states
###############################################################################
# Main Track Model Class
###############################################################################

class TrackModelApp:
    def __init__(self):
        self.red_line = TrackBackend("Red")
        self.green_line = TrackBackend("Green")
        self.outside_temp = 70.0
        self.track_heater_status = False

    def upload_track_layout_data(self, file_path):
        df = pd.read_excel(file_path)

        red_df = df[df["Line"].str.strip().str.lower() == "red"]
        green_df = df[df["Line"].str.strip().str.lower() == "green"]

        self.red_line.parse_track_layout_data(red_df)
        self.green_line.parse_track_layout_data(green_df)

        print("Successfully loaded and parsed layout for Red and Green lines.")

    def change_temperature(self, new_temp):
        try:
            new_temp = float(new_temp)
            self.outside_temp = new_temp
            self.track_heater_status = new_temp <= 36
            print(f"Updated track temperature: {new_temp}°F, Heater {'On' if self.track_heater_status else 'Off'}")
        except ValueError:
            print("Invalid temperature input.")

    def send_wayside_commanded(self, train_id, wayside_speed, wayside_authority):
        for i in range(3):
            print(f"Wayside commanded data to Train {train_id}: Speed={wayside_speed}, Authority={wayside_authority} (Send #{i+1})")

# Example usage
if __name__ == "__main__":
    track_model = TrackModelApp()
    track_model.upload_track_layout_data("Track Layout & Vehicle Data vF5.xlsx")
    track_model.change_temperature(35)

    block_key = ("Green", "A", 1)
    track_model.green_line.toggle_switch(block_key)
    track_model.green_line.toggle_railway_crossing(block_key)
    track_model.green_line.update_block_occupancy(block_key, "Occupied")
    track_model.green_line.send_beacon_data(block_key)

    track_model.send_wayside_commanded(train_id=1, wayside_speed=50, wayside_authority=500)
