
import pandas as pd
from dataclasses import dataclass
from collections import defaultdict

@dataclass()
class block:
    id: str = ""
    length: int = 0
    speed_limit: float = 0
    grade: float = 0
    underground: bool = 0
    territory: int = 0
    station: bool = 0
    switch: bool = 0
    light: bool = 0
    crossing: bool = 0
    beacon: bool = 0
    
@dataclass()
class station:
    name: str = ""
    id: str = ""
    doors: int = 0  
    
@dataclass()
class switch:
    id: str = ""
    positions: tuple = ("","")

@dataclass()
class beacon:
    id: str = ""
    data: bytearray = 0


class TrackDataClass():
    def __init__(self, filepath: str):
        """
        Initialization for the static track data.

        :param filepath: The filepath to an excel containing information about the track
        """
        dataframe = pd.read_excel(filepath, engine="openpyxl") 
        
        dictionary = {key: list(dataframe[key]) for key in dataframe.columns}
        self.line_name = dictionary["Line"][0]

        self.populate_blocks(dictionary)
        self.count_infrastructure()
        self.populate_infrastructure()
        self.count_territory()  
        
        
        
       

    def populate_blocks(self, dictionary):
        """
        Creates a list of blocks from a dictionary imported from the excel sheet

        :param dictionary: A dictionary created from a pandas dataframe of the track excel sheet
        """
        self.blocks = [block() for _ in range(len(dictionary["Block Number"]))] 

        for row, item in enumerate(self.blocks):
            item.beacon = True if dictionary["Transponder"][row] == 1 else False
            item.crossing = True if dictionary["Crossing"][row] == 1 else False 
            item.grade = dictionary["Block Grade (%)"][row]
            item.length = dictionary["Block Length (y)"][row]
            item.id = dictionary["Section"][row] + str(row + 1)
            item.speed_limit = dictionary["Speed Limit (MPH)"][row]
            item.station = True if pd.notna(dictionary["Station"][row]) else False
            item.switch = True if pd.notna(dictionary["Switch"][row]) else False
            item.underground = True if dictionary["Underground"][row] == 1 else False
            item.territory = dictionary["Territory"][row]
            item.light = True if dictionary["Light"][row] == 1 else False

    def count_infrastructure(self):
        """
        Retrieves a count for the total number of devices on the track
        """
        self.switch_count = sum(block.switch for block in self.blocks)
        self.station_count = sum(block.station for block in self.blocks)
        self.beacon_count = sum(block.beacon for block in self.blocks)
        self.light_count = sum(block.light for block in self.blocks)
        self.crossing_count = sum(block.crossing for block in self.blocks)
    
    def populate_infrastructure(self, dictionary):
        """
        Creates lists of switches, stations, beacons, lights, crossings from the excel dictionary
        :param dictionary: A dictionary created from a pandas dataframe of the track excel sheet
        """

    def count_territory(self):
        """
        Counts the number of blocks in each territory
        """
        self.territory_counts = defaultdict(int)
        for block in self.blocks:
            self.territory_counts[block.territory] += 1

if __name__=="__main__":
    track = TrackDataClass("src\Track\TrackModel\GreenLine_Layout.xlsx")    
