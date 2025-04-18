"""
Author: Connor Murray
Date: 4/1/2025
Description: 
    Defines a data structure that can extract a track layout from an excel and turn it into a usable form of lists and dictionaries
    of the blocks and infrastructure on the track
"""
import pandas as pd
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True) # makes it immutable (values should not change once read from excel)
class Section: # has an attribute to help determine the direction of travel
    increasing: int = 0 # 0 is decreasing, 1 is increasing, 2 is bidirectional with regard to the train moving over the blocks

@dataclass(frozen=True) # makes it immutable (values should not change once read from excel)
class Block: # contains unchanging information about blocks
    id: str = "" # A1, B4, C12 etc..
    length: int = 0 # length of the block in yards
    speed_limit: float = 0 # speed limit in mph
    grade: float = 0 # percent grade
    underground: bool = False # is underground
    territory: tuple = (0)# integer that is 1 based indexed for each wayside
    station: bool = False # has a station 
    switch: bool = False # has a switch
    switch_exit: bool = False # a block that a switch can fork/connect to
    light: bool = False # has a light
    crossing: bool = False # has a crossing
    beacon: bool = False # has a beacon
    
@dataclass(frozen=True)
class Station:
    name: str = "" # name of the station
    doors: int = 0  # 0 for left side, 1 for right side, 2 for both sides
    
@dataclass(frozen=True)
class Switch:
    territory: int = 0 # which wayside it corresponds to
    positions: tuple = ("","") # 0, 1 # tuple of strings containing position if false, true

@dataclass(frozen=True) # makes it immutable (values should not change once read from excel)
class SwitchExit: # the blocks a switch entrance forks out to
    switch_entrance: str # the block id of the switch entrance (chokepoint) where two ends (friends) meet

@dataclass(frozen=True)
class Light:
    territory: int = 0, # which wayside it corresponds to
    positions: tuple = ("Red","Green") # 0, 1 # tuple of strings containing position if false, true

@dataclass(frozen=True)
class Crossing:
    territory: int = 0 # which wayside it corresponds to
    positions: tuple = ("Inactive","Active") # 0, 1 # tuple of strings containing position if false, true

@dataclass(frozen=True)
class Beacon:
    data: str = ""


class TrackData():
    def __init__(self, filepath: str):
        """
        Initialization for the static track data.

        :param filepath: The filepath to an excel containing information about the track
        """
        if filepath != None:
            dataframe = pd.read_excel(filepath, engine="openpyxl", sheet_name="Sheet1")
            dataframe2 = pd.read_excel(filepath,engine="openpyxl",sheet_name="Sheet2")
            dictionary = {key: list(dataframe[key]) for key in dataframe.columns}
            dictionary2 = {key: list(dataframe2[key]) for key in dataframe2.columns}
            self.line_name = dictionary["Line"][0]

            self.populate_blocks(dictionary,dictionary2)
            self.overlaps = [] # this is a list that counts the number of overlaps, overlap count between 1-2 is in index 0, 2-3 in index 2 etc
            self.count_territory()  
        

    def populate_blocks(self, dictionary, dictionary2):
        """
        Creates a list of blocks from a dictionary imported from the excel sheet

        :param dictionary: A dictionary created from a pandas dataframe of the track excel sheet "Main sheet containing info about entire track"

        :param dictionary2: Another dictionary with information about each section
        """
        self.blocks = [] # list that contains every block's (a struct) properties indexed 0 - 149 for green line
        self.switches = {} # a dictionary that allows lookup of a switch at a certain block id, if block.switch: switch[block.id].position(0), is equivalent to getting the switches position when plc outputs false
        self.switch_exits = {} # the blocks that the switch
        self.stations = {}
        self.lights = {}
        self.crossings = {} 
        self.beacons = {}
        self.SPAWN_BLOCK = ""
        self.DESPAWN_BLOCK = ""
        

        for row in range(len(dictionary["Block Number"])):
            block_id = dictionary["Section"][row] + str(row + 1)
            if isinstance(dictionary["Territory"][row], str):
                territories = dictionary["Territory"][row].split(",")
                territories = tuple([int(t.strip()) for t in territories])
            else:
                territories = dictionary["Territory"][row]

            # Create Block object
            block = Block(
                id=block_id,
                switch=pd.notna(dictionary["Switch"][row]),
                station=pd.notna(dictionary["Station"][row]),
                beacon=dictionary["Beacon"][row] == 1,
                light=dictionary["Light"][row] == 1,
                crossing=dictionary["Crossing"][row] == 1,
                underground=dictionary["Underground"][row] == 1,
                grade=dictionary["Block Grade (%)"][row],
                length=dictionary["Block Length (y)"][row],
                speed_limit=dictionary["Speed Limit (MPH)"][row],
                territory=territories,
                switch_exit=pd.notna(dictionary["Switch Exit"][row])
            )

            self.blocks.append(block)

            # Create and store objects that will go into the corresponding dictionaries (devices like switches and lights only need to know their first territory)
            if isinstance(territories, tuple):
                switch_obj = self.parse_switch(dictionary["Switch"][row], territories[0])
                light_obj = Light(territory=territories[0]) if dictionary["Light"][row] == 1 else None
                crossing_obj = Crossing(territory=territories[0]) if dictionary["Crossing"][row] else None
                beacon_obj = Beacon(data=dictionary["Beacon Data"][row]) if dictionary["Beacon"][row] else None
                station_obj = self.parse_station(dictionary["Station"][row], dictionary["Station Side"][row])
            else:
                switch_obj = self.parse_switch(dictionary["Switch"][row], territories)
                light_obj = Light(territory=territories) if dictionary["Light"][row] == 1 else None
                crossing_obj = Crossing(territory=territories) if dictionary["Crossing"][row] else None
                beacon_obj = Beacon(data=dictionary["Beacon Data"][row]) if dictionary["Beacon"][row] else None
                station_obj = self.parse_station(dictionary["Station"][row], dictionary["Station Side"][row])

            if switch_obj:
                self.switches[block_id] = switch_obj
            if light_obj:
                self.lights[block_id] = light_obj
            if crossing_obj:
                self.crossings[block_id] = crossing_obj
            if station_obj:
                self.stations[block_id] = station_obj
            if beacon_obj:
                self.beacons[block_id] = beacon_obj

            if pd.notna(dictionary["Switch Exit"][row]) == True:
                switch_exit_obj = SwitchExit(switch_entrance=dictionary["Switch Exit"][row])
                self.switch_exits[block_id] = switch_exit_obj

        if self.blocks[-2].id[0]=='y':
            self.SPAWN_BLOCK = self.blocks[-2]
            self.DESPAWN_BLOCK = self.blocks[-1]
        else:
            self.SPAWN_BLOCK = self.DESPAWN_BLOCK = self.blocks[-1]

        self.sections = {}

        for row in range(len(dictionary2["Section"])):
            section = Section(dictionary2["Increasing"][row])
            self.sections[dictionary2["Section"][row]]=section

        
        
    def parse_switch(self, value: str, territory: int):
        """
        Parses a switch column entry into an immutable Switch object.

        :param value: The entry into the switch column containing the two positions of the switches
        
        :param territory: The corresponding territory in excel sheet
        """
        if pd.isna(value):  # Handle missing values
            return None  # No switch exists

        parts = str(value).split(",")  # Split on comma
        parts = [p.strip() for p in parts]  # Remove spaces

        # Ensure the positions tuple is of size 2
        if len(parts) == 1:
            positions = (parts[0], "")
        elif len(parts) >= 2:
            positions = (parts[0], parts[1])
        else:
            positions = ("", "")

        return Switch(territory=territory, positions=positions)
    
    def parse_station(self, value1: str, value2: int):
        """
        Parses a switch column entry into an immutable Switch object.

        :param value1: is the name of the station from the excel sheet

        :param value1: is the side the door is on, 0 - left, 1 - right, 2 - both
        """

        if pd.isna(value1) and pd.isna(value2):
            return None
        
        name = str(value1) 
        door = int(value2)

        return Station(name=name,doors=door)

    def count_territory(self):
        """
        Counts the number of blocks, switches, lights and crossings in each wayside territory
        """
        # Using default dictionary so that key errors do not occur when adding in elements with keys that have not been created before
        temp_territory_counts = defaultdict(int)
        temp_device_counts = defaultdict(lambda: {"switches": 0, "lights": 0, "crossings": 0})
        # Iterate through blocks and count the number of blocks in each territory
        for block in self.blocks:
            if isinstance(block.territory, tuple):
                if block.territory[0] > len(self.overlaps):
                    self.overlaps.append(0)
                for t in block.territory:
                    temp_territory_counts[t] += 1

                temp_device_counts[block.territory[0]]["switches"] += block.switch # should never happen though since overlaps shouldn't have devices?
                temp_device_counts[block.territory[0]]["lights"] += block.light
                temp_device_counts[block.territory[0]]["crossings"] += block.crossing
                self.overlaps[block.territory[0] - 1] += 1
            else:
                temp_territory_counts[block.territory] += 1
                temp_device_counts[block.territory]["switches"] += block.switch
                temp_device_counts[block.territory]["lights"] += block.light
                temp_device_counts[block.territory]["crossings"] += block.crossing

        # convert back to regular dictionaries
        self.territory_counts = dict(temp_territory_counts)
        self.device_counts = {k: dict(v) for k, v in temp_device_counts.items()} 
        
def init():
    global lines 
    lines = {}
    line = TrackData("src/Track/TrackModel/GreenLine_Layout.xlsx")
    lines[line.line_name] = line

if __name__ == "__main__":
    init()