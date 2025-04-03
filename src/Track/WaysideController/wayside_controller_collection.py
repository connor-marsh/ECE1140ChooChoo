"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that contains several WaysideControllers and a Frontend. Responsible for interfacing with the Track Model and CTC
"""
import sys
import globals.track_data_class as init_track_data
import globals.signals as signals
from Track.WaysideController.wayside_controller_backend import WaysideController
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
        if track_model != None:
            if track_model.name not in init_track_data.lines:
                raise KeyError
            self.track_model = track_model
            self.LINE_NAME = track_model.name
            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.update_track_model)
        else:
            if line_name not in init_track_data.lines:
                raise KeyError
            self.LINE_NAME = line_name

        # get references to the data from the corresponding track
        track_data = init_track_data.lines[self.LINE_NAME]
        self.blocks = track_data.blocks 
        self.switches = track_data.switches # dictionaries don't require sorting duh
        self.lights = track_data.lights
        self.crossings = track_data.crossings

        self.controllers = [] # A collection of wayside has controllers
        self.CONTROLLER_COUNT = len(track_data.territory_counts) # get the number of controllers (CONSTANT)

        self.blocks.sort(key=lambda block: (block.territory, block.id[0], int(block.id[1:]))) # sort blocks by territory then by section then by number

        # Will get the number corresponding to each wayside controller below (CONSTANTS)
        self.BLOCK_COUNTS = [] 
        self.SWITCH_COUNTS = []
        self.LIGHT_COUNTS = []
        self.CROSSING_COUNTS = []

        for i in range(self.CONTROLLER_COUNT): # for each controller they will have a specific number of blocks, switches, lights, and crossings associated with it
            block_count = track_data.territory_counts[i + 1]
            switch_count = track_data.device_counts[i + 1]['switches']
            light_count = track_data.device_counts[i + 1]['lights']
            crossing_count = track_data.device_counts[i + 1]['crossings']
            self.BLOCK_COUNTS.append(block_count)
            self.SWITCH_COUNTS.append(switch_count)
            self.LIGHT_COUNTS.append(light_count)
            self.CROSSING_COUNTS.append(crossing_count)
            self.controllers.append(WaysideController(block_count=block_count,switch_count=switch_count,
                                                      light_count=light_count,crossing_count=crossing_count,exit_block_count=0))

        # Get the ranges of each territory, so that indexing the list is easier
        self.BLOCK_RANGES = self.get_ranges(self.BLOCK_COUNTS)
        self.SWITCH_RANGES = self.get_ranges(self.SWITCH_COUNTS)
        self.LIGHT_RANGES = self.get_ranges(self.LIGHT_COUNTS)
        self.CROSSING_RANGES = self.get_ranges(self.CROSSING_COUNTS)

        # Create a list of testbenches for maintenance mode corresponding to each one of the wayside controllers
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerTestbench # Avoiding circular imports?
        self.testbenches = [WaysideControllerTestbench(collection_reference=self,idx=i) for i in range(self.CONTROLLER_COUNT)]

        # Initialize the frontend with access to the collection so that it may modify itself or the backend using the data from the backend
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerFrontend # lazy import to avoid circular import (do NOT tell me about design patterns)
        self.frontend = WaysideControllerFrontend(self, auto_import_programs)
        

        self.connect_signals()
    
    def get_ranges(self, counts): # THIS FUNCTION COULD BE MOVED TO THE TRACK DATA CLASS BUT THIS KINDA FITS MORE WITH WHAT I HAVE TO DO (ONLY USED FOR INIT)
        """
        Given a list of counts per territory, compute the start and end indices. 
        
        :param counts: List of the number of blocks per territory ie. [50,30,40] indicates 50 blocks for wayside 1, 30 blocks for wayside 2 and so on

        :return: List of [start, end) index tuples. Start inclusive end not inclusive.
        """
        ranges = []
        start_index = 0  # 0 based indexing
        for count in counts:
            end_index = start_index + count - 1  # Last element in this range
            ranges.append((start_index, end_index + 1))
            start_index = end_index + 1  # Move start index to next range
        return ranges

    @pyqtSignal()
    def update_track_model(self):
        """
        Sends the outputs of each controller's plc program upon the collection's timer timing outs
        """

        switch_states = []
        light_states = []
        crossing_states = []

        # append each controller's outputs
        for controller in self.collection.controllers:
            switch_states = switch_states + controller.switch_positions
            light_states = light_states + controller.light_signals
            crossing_states = crossing_states + controller.crossing_signals

        # send the outputs along with the sorted block struct so that they can interpret the values
        self.track_model.update_from_plc_outputs(self.blocks, switch_states, light_states, crossing_states)


    @pyqtSlot(str, bool)
    def handle_switch_maintenance(block_id, position):
        """
        This function is called when the ctc makes a request to change a switch a position

        :param block_id: The id of the block with the switch

        :param position: The requested position to change the switch to
        """
    
    @pyqtSlot(list)
    def handle_exit_blocks(current_exit_blocks):
        """
        Called when the ctc sends what the exit blocks are. Does stuff for exit blocks?

        :param current_exit_blocks: A list of vectors per wayside controller indicating the active exit block
        """

    @pyqtSlot()
    def handle_dispatch():
        """
        Called when the ctc dispatches a train. Verifies that it is safe to dispatch the train
        """
        # check if it is safe to dispatch the train
        # call track model's method for creating a new train

    @pyqtSlot(int, bool)
    def handle_block_maintenance(block_number, state):
        """
        Called when the ctc puts a block into maintenance

        :param block_number: the index into the block list

        :param state:  0 for maintenance off, 1 for maintenance on
        """
    @pyqtSlot(list,list)
    def handle_suggested_values(speeds, authorities):
        """
        Called when the ctc sends suggested speeds and suggested authorities

        :param speeds: a list of suggested speeds from the ctc

        :param authorities: a list of suggested authoritities from the ctc
        """

    def connect_signals(self): # may still need this when using signals later
        """
        Connects any necessary signals for communication using the pyqt framework
        """
        signals.communication.ctc_switch_maintenance.connect(self.handle_switch_maintenance)
        signals.communication.ctc_exit_blocks.connect(self.handle_exit_blocks)
        signals.communication.ctc_dispatch.connect(self.handle_dispatch)
        signals.communication.ctc_block_maintenance.connect(self.handle_block_maintenance)
        signals.communication.ctc_suggested.connect(self.handle_suggested_values)

    #DEFINE A FUNCTION THAT EITHER GRABS VALUES FROM THE TRACK REFERENCE OR FROM THE TESTBENCH DEPENDING ON THE MODE OF THE CONTROLLER
    # FOR EACH CONTROLLER CHECK THE MODE 
    # READ EACH VALUE FROM TRACK MODEL EVERY UPDATE IF NOT IN MAINTENANCE MODE
    # OTHERWISE ONCE TESTBENCH WRITES A NEW VALUE TO THE WAYSIDE
    # WHEN EXITING RESET MAINTENANCE (DONE) RESET THE BACKEND VALUES (EASY) RESET THE TESTBENCH VALUES ( i guess choose whatever is easier?)
