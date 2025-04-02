import sys
import os
import random
import pandas as pd
from Track.TrackModel.track_model_enums import Occupancy, Failures
from globals.track_data_class import TrackDataClass
from PyQt5 import QtWidgets, QtCore

# Import the UI files generated from Qt Designer
from Track.TrackModel.track_model_ui import Ui_MainWindow as TrackModelUI
from Track.TrackModel.test_bench_track_model import Ui_MainWindow as TBTrackModelUI

from Train.train_collection import TrainCollection

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
# Dummy Train Class
###############################################################################

class Train:
    def __init__(self, train_id, initial_block: str):
        self.train_id = train_id
        self.current_block = initial_block
        self.distance_traveled = 0.0
        self.passenger_count = 0
        self.travel_direction = 0 # CHANGE THIS MOST LIKELY
        self.train_model = None

    def update(self):
        distance_within_block = self.train_model.position - self.distance_traveled
        # if distance within block > length of block
        # then update_location(new_block=bloc, distance_delta=distance_within_block)
        if distance_within_block > self.block.length:
            pass
            # implement still

        
    def update_location(self, new_block: str, distance_delta: float):
        self.current_block = new_block
        self.distance_traveled += distance_delta

    def board_passengers(self, count: int):
        self.passenger_count += count

    def __str__(self):
        return (f"Train {self.train_id} | Block: {self.current_block} | "
                f"Distance: {self.distance_traveled:.2f} | Passengers: {self.passenger_count}")



###############################################################################
# Track BackEnd
###############################################################################

class TrackModel(QtWidgets.QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.runtime_status = {} # Runtime status of blocks
        self.trains = []  # Key: holds Train instances
        self.train_counter = 0
        self.train_collection = TrainCollection()

        self.prev_time = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

    def update(self):
        self.update_train_collection()

    # Populating the trains with information sent from train
    def update_train_collection(self):
        for train in self.trains:
            data = {self.send_wayside_commanded, self.send_beacon_data, self.block.grade, self.station.passengers} # Need to update wayside func
            # put in wayside speed, wayside authority (only if new value), beacon data (if it exists), grade, passengers
            train.train_model.set_input_data(wayside_data=data)
            train.update()

    # Parsing data sent from main track file
    def parse_track_layout_data(self, filepath):
        """
        Loads and parses track layout using the TrackDataClass. - add params
        """
        self.track_data = TrackDataClass(filepath)
        print(f"[{self.name}] Loaded layout for {self.track_data.line_name} line.")
        print(f"  Total Blocks: {len(self.track_data.blocks)}")
        for territory, blocks in self.track_data.territory_counts.items():
            devices = self.track_data.device_counts[territory]
            print(f"  Territory {territory}: {blocks} blocks, {devices['switches']} switches, "
                f"{devices['lights']} lights, {devices['crossings']} crossings")

    # Updating switches, lights, and railway crossings sent from wayside
    def update_from_wayside_outputs(self, controller_index, switch_states, light_states, crossing_states):
        block_ids = self.track_data.controller_territory[controller_index]

    # Updating switch position , should display the proper next block
    # XOR with current position list and compare to see if update
        switch_keys = [bid for bid in block_ids if bid in self.track_data.switches]
        for i, state in enumerate(switch_states):
            if i < len(switch_keys):
                block_id = switch_keys[i]
                direction = "higher-numbered" if state else "lower-numbered"
                print(f"[Wayside Update] Switch at Block {block_id} set to {direction} connection.")

    # Updating light states, should display green/red
    # XOR with current position list and compare to see if update
        light_keys = [bid for bid in block_ids if bid in self.track_data.lights]
        for i, state in enumerate(light_states):
            if i < len(light_keys):
                block_id = light_keys[i]
                color = "Green" if state else "Red"
                print(f"[Wayside Update] Light at Block {block_id} turned {color}.")

    # Updating railway crossing position, should display if open/closed
    # XOR with current position list and compare to see if update
        crossing_keys = [bid for bid in block_ids if bid in self.track_data.crossings]
        for i, state in enumerate(crossing_states):
            if i < len(crossing_keys):
                block_id = crossing_keys[i]
                status = "ACTIVE (train approaching)" if state else "INACTIVE (safe for cars)"
                print(f"[Wayside Update] Crossing at Block {block_id} is now {status}.")

    # Updating block occupancies, should read if train, maintenance, or failure is there
    # OR with train, maintenance, and failures
    # Should dynamically update
    def update_block_occupancy(self, block_id: str, status: str):

        if not any(b.id == block_id for b in self.track_data.blocks):
            print(f"[Occupancy Update] Block {block_id} not found in static layout.")
            return

        try:
            occupancy_enum = Occupancy[status.upper()]
        except KeyError:
            print(f"[Occupancy Update] Invalid occupancy status: {status}")
            return

        self.runtime_status.setdefault(block_id, {})
        self.runtime_status[block_id]["occupancy"] = occupancy_enum

        failure = self.runtime_status[block_id].get("failure", Failures.NONE)
        derived_occupied = (
            occupancy_enum in [Occupancy.OCCUPIED, Occupancy.MAINTENANCE]
            or failure != Failures.NONE
        )
        self.runtime_status[block_id]["is_occupied_display"] = derived_occupied

        print(f"[Occupancy Update] Block {block_id} status = {occupancy_enum.name} -> Display as {'OCCUPIED' if derived_occupied else 'UNOCCUPIED'}")

    #  Sends beacon data when a train is on the specific block
    def send_beacon_data(self, block_id: str):
        # Check if a train is on this block
        train_on_block = any(train.current_block == block_id for train in self.trains.values())
        if not train_on_block:
            print(f"[Beacon] No train present on {block_id}. Beacon not sent.")
            return

        # Check if the block has a beacon
        if block_id not in self.track_data.beacons:
            print(f"[Beacon] Block {block_id} does not contain a transponder.")
            return

        # Encode and store beacon data
        beacon_data = f"Beacon: Block {block_id}".encode()
        self.runtime_status.setdefault(block_id, {})
        self.runtime_status[block_id]["beacon_data"] = beacon_data

        print(f"[Beacon] Beacon data sent on block {block_id}: {beacon_data.decode()}")

        return beacon_data

    # WIP - probably going to delete,Sending section data to frontend, can probably scrap
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

    # Sends block information
    # Returns the Block for the specified block key
    def send_block_data(self, block_id_str):
        block = next((b for b in self.track_data.blocks if b.id == block_id_str), None)
        if not block:
            print(f"[{self.name}] Block {block_id_str} not found.")
            return None

        return {
            "block_id": block.id,
            "length": block.length,
            "grade": block.grade,
            "speed_limit": block.speed_limit,
            "underground": block.underground,
            "station": block.station,
            "switch": block.switch,
            "light": block.light,
            "crossing": block.crossing,
            "beacon": block.beacon,
            "occupancy": self.runtime_status.get(block.id, {}).get("occupancy", Occupancy.UNOCCUPIED).name,
            "failure": self.runtime_status.get(block.id, {}).get("failure", Failures.NONE).name,
            "is_occupied_display": self.runtime_status.get(block.id, {}).get("is_occupied_display", False),
        }

        
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

    # Initializing a train - somewhat WIP not sure if it works yet
    # Wayside will call when to initialize a train
    def initialize_train(self):
        start_block = "GreenK63"
        
        # Verify block exists
        if not any(b.id == start_block for b in self.track_data.blocks):
            print(f"[Train Init] Block {start_block} not found in static layout.")
            return

        # Increment and assign new train
        self.train_counter += 1
        train_id = self.train_counter-1
        new_train = Train(train_id=train_id, current_block=start_block)
        self.train_collection.createTrain()
        new_train.train_model = self.train_collection.train_list[-1]

        # Store train in backend registry
        self.trains.append(new_train)

        # Mark the block as occupied
        self.update_block_occupancy(start_block, "Occupied")

        print(f"[Train Init] Train {train_id} initialized on {start_block}.")

        # WIP should initialize train UI

    
    # Ensure the train is travelling the proper direction (ascending or descending)
    def train_travel_direction(self, train_id, current_section):
        # Get current section's direction
        current_direction = current_section.direction

        # Get previous section from train stored state
        previous_section = self.previous_section.get(train_id, ) # add variable

        # Decide the proper travel direction
        if current_direction == 2 and previous_section == 0:
            travel_direction = 1  # Going descending
            print(f"Train {train_id} is traveling descending (A -> D).")

        elif current_direction == 2 and previous_section == 1:
            travel_direction = 0  # Going ascending
            print(f"Train {train_id} is traveling ascending (Z -> F).")

        elif previous_section == 2 and current_direction == 1:
            travel_direction = 1  # Continue descending
            print(f"Train {train_id} is continuing descending.")

        elif previous_section == 2 and current_direction == 0:
            travel_direction = 0  # Continue ascending
            print(f"Train {train_id} is continuing ascending.")

        else:
            # Default: keep going same direction
            travel_direction = current_direction
            print(f"Train {train_id} continues in direction {travel_direction}.")

        # Update the train's previous section
        self.previous_section[train_id] = current_section

        return travel_direction
    
            

###############################################################################
# Track FrontEnd
###############################################################################

# Initializing UI

# WIP When a section is clicked, zoom in (may scrap)
    def load_section(self, section_id, line):
        if line.lower() == "green":
            block_ids = self.backend.green_line.send_section_data(section_id)
        else:
            block_ids = self.backend.red_line.send_section_data(section_id)

# WIP When a block is clicked, display block information
    def load_block(self, block_id, line):
        if line.lower() == "green":
            block_data = self.backend.green_line.send_block_data(block_id)
        else:
            block_data = self.backend.red_line.send_block_data(block_id)


