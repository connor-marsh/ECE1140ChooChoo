import sys
import os
import random
import pandas as pd
from Track.TrackModel.track_model_enums import Occupancy, Failures
import globals.track_data_class as global_track_data
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
# Dynamic Track Class
###############################################################################

# class Block:
#     def __init__(self, block_id, length, grade, speed_limit, elevation, cumulative_elevation, infrastructure, station_side):
#         self.block_id = block_id
#         self.length = length
#         self.grade = grade
#         self.speed_limit = speed_limit
#         self.elevation = elevation
#         self.cumulative_elevation = cumulative_elevation
#         self.infrastructure = infrastructure
#         self.station_side = station_side
#         self.occupancy = Occupancy.UNOCCUPIED
#         self.failures = Failures.NONE
#         self.switch_state = False
#         self.railway_signal = False
#         self.traffic_signal = "None"
#         self.beacon_data = None
class DynamicTrack:
    def __init__(self):
        self.occupancies = {}
        self.switch_states = {}
        self.light_states = {}
        self.crossing_states = {}
        self.failures = {}

###############################################################################
# Dummy Train Class
###############################################################################

class Train:
    def __init__(self, train_id, track_model=None, initial_block=None):
        self.track_data = track_model.track_data
        self.dynamic_track = track_model.dynamic_track
        self.train_id = train_id
        self.current_block = initial_block
        self.current_section = initial_block.id[0] # just a string
        self.entered_new_section = True
        self.distance_traveled = 0.0
        self.passenger_count = 0
        # FIX THIS FOR RED LINE
        self.travel_direction = self.track_data.sections[self.current_section].increasing # This gets updated when switching sections
        self.train_model = None

    def update(self):
        train_position = self.train_model.get_output_data()["position"]
        distance_within_block = train_position - self.distance_traveled
        if distance_within_block > self.current_block.length:
            self.distance_traveled += self.current_block.length
            self.entered_new_section = False
            # Set old block to unoccupied
            self.dynamic_track.occupancies[self.current_block.id]=Occupancy.UNOCCUPIED
            # Move to new block
            if self.current_block.switch and not self.entered_new_section:
                print("SWITCH")
                switch = self.track_data.switches[self.current_block.id]
                switchState=self.dynamic_track.switch_states[self.current_block.id]
                self.current_block = self.track_data.blocks[int(switch.positions[1 if switchState else 0].split("-")[1])-1]
            elif self.current_block.switch_exit and not self.entered_new_section:
                print("SWITCH")
                switch = self.track_data.switches[self.track_data.switch_exits[self.current_block.id].switch_entrance]
                switchState=self.dynamic_track.switch_states[self.track_data.switch_exits[self.current_block.id].switch_entrance]
                switchBlocks = switch.positions[1 if switchState else 0].split("-")
                if switchBlocks[1] == self.current_block.id[1:]:
                    self.current_block = self.track_data.blocks[int(switchBlocks[0])-1]
                else:
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
                    print("TRAIN CRASH FROM SWITCH POSITION")
            else:
                self.current_block = self.track_data.blocks[int(self.current_block.id[1:])+(self.travel_direction*2-1)-1]
            
            # Set new block to occupied
            self.dynamic_track.occupancies[self.current_block.id]=Occupancy.OCCUPIED

            # Check for beacon data in new block, if its there, send to train model
            if self.track_data.blocks[self.current_block.id].beacon:
                send_to_train = {}
                send_to_train["beacon_data"] = self.track_data.beacons[self.current_block.id].data
                self.train_model.set_input_data(track_data=send_to_train)

            # Check for station in new block, if its there, add and remove passengers from train
            # TODO

            # Move to new section
            if self.current_block.id[0] != self.current_section:
                print("New section")
                self.entered_new_section = True
                increasing = self.track_data.sections[self.current_block.id[0]].increasing
                if increasing == 2:
                    self.travel_direction = 1 if self.current_block.id[0] > self.current_section else 0
                else:
                    self.travel_direction = increasing
                self.current_section = self.current_block.id[0]
                if self.current_section == "O":
                    self.dynamic_track.switch_states["N85"] = True
                
            print("BLOCK: " + self.current_block.id)

        
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
        self.track_data = global_track_data.lines[name]
        self.runtime_status = {} # Runtime status of blocks
        self.trains = []  # holds Train instances
        self.train_counter = 0
        self.train_collection = TrainCollection()

        # Populate dynamic track
        self.dynamic_track = DynamicTrack()
        for block in self.track_data.blocks:
            self.dynamic_track.occupancies = Occupancy.UNOCCUPIED
            if block.switch:
                self.dynamic_track.switch_states[block.id] = False
            if block.light:
                self.dynamic_track.light_states[block.id] = False
            if block.crossing:
                self.dynamic_track.crossing_states[block.id] = False

        self.initialize_train()

        self.prev_time = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        

    def update(self):
        self.update_trains()

    # Populating the trains with information sent from train
    def update_trains(self):
        for train in self.trains:
            train.update()

    # Parsing data sent from main track file
    def parse_track_layout_data(self, filepath):
        """
        Loads and parses track layout using the TrackDataClass. - add params
        """
        pass
        # INCOMPLETE
        # self.track_data.update(filepath) # ACTUALLY DO

    # Updating switches, lights, and railway crossings sent from wayside
    def update_from_plc_outputs(self, sorted_blocks, switch_states, light_states, crossing_states):
        pass

        # Updating switch position , should display the proper next block
        # XOR with current position list and compare to see if update
        switch_keys = [block.id for block in sorted_blocks if block.switch]
        for i, state in enumerate(switch_states):
            if i < len(switch_keys):
                self.dynamic_track.switch_states[switch_keys[i]]=state
                # direction = "higher-numbered" if state else "lower-numbered"
                # print(f"[Wayside Update] Switch at Block {switch_keys[i]} set to {self.track_data.switches[switch_keys[i].positions[1 if state else 0]]} connection.")

        # Updating light states, should display green/red
        # XOR with current position list and compare to see if update
        light_keys = [block.id for block in sorted_blocks if block.light]
        for i, state in enumerate(light_states):
            if i < len(light_keys):
                self.dynamic_track.light_states[light_keys[i]]=state
                # color = "Green" if state else "Red"
                # print(f"[Wayside Update] Light at Block {light_keys[i]} turned {color}.")

        # Updating railway crossing position, should display if open/closed
        # XOR with current position list and compare to see if update
        crossing_keys = [block.id for block in sorted_blocks if block.crossing]
        for i, state in enumerate(crossing_states):
            if i < len(crossing_keys):
                self.dynamic_track.crossing_states[crossing_keys[i]]=state
                # status = "ACTIVE (train approaching)" if state else "INACTIVE (safe for cars)"
                # print(f"[Wayside Update] Crossing at Block {crossing_keys[i]} is now {status}.")

    def update_from_comms_outputs(self, wayside_speeds={}, wayside_authorities={}, maintenances={}):
        for train in self.trains:
            send_to_train = {} # conglomerate in this to prevent calling set_input_data multiple times
            if train.current_block.id in wayside_speeds:
                send_to_train["wayside_speed"]=wayside_speeds[train.current_block.id]
            if train.current_block.id in wayside_speeds:
                send_to_train["wayside_authority"]=wayside_authorities[train.current_block.id]
            if len(send_to_train)>0:
                train.train_model.set_input_data(track_data=send_to_train)
        for block, maintenance in maintenances.items():
            if maintenance:
                self.dynamic_track.occupancies[block]=Occupancy.MAINTENANCE
            else:
                self.dynamic_track.occupancies[block]=Occupancy.UNOCCUPIED

        
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

    # Wayside will call when to initialize a train
    def initialize_train(self):
        start_block = self.track_data.blocks[63-1]
        
        # Verify block exists
        # if not any(b.id == start_block for b in self.track_data.blocks):
        #     print(f"[Train Init] Block {start_block} not found in static layout.")
        #     return

        # Increment and assign new train
        self.train_counter += 1
        train_id = self.train_counter-1
        new_train = Train(train_id=train_id, track_model=self, initial_block=start_block)
        self.train_collection.createTrain()
        new_train.train_model = self.train_collection.train_list[-1]

        # Store train in backend registry
        self.trains.append(new_train)

        # Mark the block as occupied
        self.update_block_occupancy(start_block, "Occupied")

        print(f"[Train Init] Train {train_id} initialized on {start_block}.")

    
    # Ensure the train is travelling the proper direction (ascending or descending)
    # def train_travel_direction(self, train_id, current_section):
    #     # Get current section's direction
    #     current_direction = current_section.direction

    #     # Get previous section from train stored state
    #     previous_section = self.previous_section.get(train_id, ) # add variable

    #     # Decide the proper travel direction
    #     if current_direction == 2 and previous_section == 0:
    #         travel_direction = 1  # Going descending
    #         print(f"Train {train_id} is traveling descending (A -> D).")

    #     elif current_direction == 2 and previous_section == 1:
    #         travel_direction = 0  # Going ascending
    #         print(f"Train {train_id} is traveling ascending (Z -> F).")

    #     elif previous_section == 2 and current_direction == 1:
    #         travel_direction = 1  # Continue descending
    #         print(f"Train {train_id} is continuing descending.")

    #     elif previous_section == 2 and current_direction == 0:
    #         travel_direction = 0  # Continue ascending
    #         print(f"Train {train_id} is continuing ascending.")

    #     else:
    #         # Default: keep going same direction
    #         travel_direction = current_direction
    #         print(f"Train {train_id} continues in direction {travel_direction}.")

    #     # Update the train's previous section
    #     self.previous_section[train_id] = current_section

    #     return travel_direction
    
            

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


