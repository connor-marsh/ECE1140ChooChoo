"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that contains several WaysideControllers and a Frontend. Responsible for interfacing with the Track Model and CTC
"""
import sys
import globals.track_data_class as init_track_data
import globals.signals as signals
from Track.TrackModel.track_model_enums import Occupancy
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject, QTimer

class WaysideControllerCollection(QObject):
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class.
    """

    def __init__(self, track_model=None, line_name="Green", auto_import_programs=True):
        """
        :param track_data: A class that contains the unchanging data imported from the track builder
        """
        super().__init__()
        self.track_model = track_model
        if track_model != None:
            if track_model.name not in init_track_data.lines:
                raise KeyError
            
            self.LINE_NAME = track_model.name
        else:
            if line_name not in init_track_data.lines:
                raise KeyError
            self.LINE_NAME = line_name


        # get references to the data from the corresponding track
        self.track_data = init_track_data.lines[self.LINE_NAME]
        self.overlaps = self.track_data.overlaps
        self.switches = self.track_data.switches # dictionaries don't require sorting duh
        self.lights = self.track_data.lights
        self.crossings = self.track_data.crossings

        self.controllers = [] # A collection of wayside has controllers
        self.CONTROLLER_COUNT = len(self.track_data.territory_counts) # get the number of controllers (CONSTANT)

        # my blocks are a list of lists i filter the main list by territory and then i use ranges to index them in my ui
        self.blocks = [self.get_blocks_for_territory(i + 1, self.track_data.blocks) for i in range(self.CONTROLLER_COUNT)]

        # Will get the number corresponding to each wayside controller below (CONSTANTS)
        self.BLOCK_COUNTS = [] 
        self.SWITCH_COUNTS = []
        self.LIGHT_COUNTS = []
        self.CROSSING_COUNTS = []

        from Track.WaysideController.wayside_controller_backend import WaysideController # lazy import
        for i in range(self.CONTROLLER_COUNT): # for each controller they will have a specific number of blocks, switches, lights, and crossings associated with it
            block_count = self.track_data.territory_counts[i + 1]
            switch_count = self.track_data.device_counts[i + 1]['switches']
            light_count = self.track_data.device_counts[i + 1]['lights']
            crossing_count = self.track_data.device_counts[i + 1]['crossings']
            self.BLOCK_COUNTS.append(block_count)
            self.SWITCH_COUNTS.append(switch_count)
            self.LIGHT_COUNTS.append(light_count)
            self.CROSSING_COUNTS.append(crossing_count)
            self.controllers.append(WaysideController(block_count=block_count,switch_count=switch_count,
                                                      light_count=light_count,crossing_count=crossing_count,
                                                      exit_block_count=0, index=i, collection_reference=self))

        # Get the ranges of each territory, so that indexing the list is easier
        self.BLOCK_RANGES = self.get_ranges_with_overlap(self.BLOCK_COUNTS,self.overlaps)
        #self.SWITCH_RANGES = self.get_ranges(self.SWITCH_COUNTS)
        #self.LIGHT_RANGES = self.get_ranges(self.LIGHT_COUNTS)
        #self.CROSSING_RANGES = self.get_ranges(self.CROSSING_COUNTS)

        # Create a list of testbenches for maintenance mode corresponding to each one of the wayside controllers
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerTestbench # Avoiding circular imports?
        self.testbenches = [WaysideControllerTestbench(collection_reference=self,idx=i) for i in range(self.CONTROLLER_COUNT)]

        # Initialize the frontend with access to the collection so that it may modify itself or the backend using the data from the backend
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerFrontend # lazy import to avoid circular import (do NOT tell me about design patterns)
        self.frontend = WaysideControllerFrontend(self, auto_import_programs)
        

        self.connect_signals()


    def get_sort_territory(self, territory):
        if isinstance(territory, int):
            return (territory, 1)  # normal territory, secondary sort to put them before overlap
        elif isinstance(territory, tuple):
            return (territory[0], 2)  # overlap — put after main territory
    
    def get_blocks_for_territory(self, territory, blocks):
        # Assuming block.territory can be an int or a tuple, or even a list.
        filtered = [
            block for block in blocks
            if (isinstance(block.territory, (tuple, list)) and territory in block.territory) or
            (block.territory == territory)
        ]
        return filtered
    
    
    def get_ranges_with_overlap(self, counts, overlaps):
        """
        Compute the contiguous block ranges for each territory, 
        accounting for overlaps between consecutive territories.

        :param counts: List of number of blocks for each territory. 
                    For example, [50, 40, 30] means territory 0 has 50 blocks, 
                    territory 1 has 40 blocks, territory 2 has 30 blocks.
        :param overlaps: List of overlap counts between each territory and the next.
                        For example, [10, 5] means territory 0 and 1 overlap by 10 blocks,
                        and territory 1 and 2 overlap by 5 blocks.
        :return: List of (start, end) tuples for each territory. End is non-inclusive.
        """
        if len(overlaps) != len(counts) - 1:
            raise ValueError("Length of overlaps must be one less than length of counts.")

        ranges = []
        # The first territory always starts at index 0.
        start_index = 0
        for i, count in enumerate(counts):
            end_index = start_index + count
            ranges.append((start_index, end_index))
            # If there is another territory, subtract the appropriate overlap
            if i < len(overlaps):
                start_index = end_index - overlaps[i]
        return ranges



    
    
    @pyqtSlot()
    def handle_dispatch(self):
        """
        Called when the ctc dispatches a train. Verifies that it is safe to dispatch the train
        """
        if self.track_model != None:
            if self.track_model.dynamic_track.occupancies[self.track_model.track_data.SPAWN_BLOCK.id] == Occupancy.UNOCCUPIED:
                self.track_model.initialize_train()

        


  
            

    def connect_signals(self): # may still need this when using signals later
        """
        Connects any necessary local and global signals for communication using the pyqt framework
        """
        signals.communication.ctc_dispatch[self.LINE_NAME].connect(self.handle_dispatch)
 




    #DEFINE A FUNCTION THAT EITHER GRABS VALUES FROM THE TRACK REFERENCE OR FROM THE TESTBENCH DEPENDING ON THE MODE OF THE CONTROLLER
    # FOR EACH CONTROLLER CHECK THE MODE 
    # READ EACH VALUE FROM TRACK MODEL EVERY UPDATE IF NOT IN MAINTENANCE MODE
    # OTHERWISE ONCE TESTBENCH WRITES A NEW VALUE TO THE WAYSIDE
    # WHEN EXITING RESET MAINTENANCE (DONE) RESET THE BACKEND VALUES (EASY) RESET THE TESTBENCH VALUES ( i guess choose whatever is easier?)
