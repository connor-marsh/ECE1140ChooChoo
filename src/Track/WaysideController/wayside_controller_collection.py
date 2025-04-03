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
        track_data = init_track_data.lines[self.LINE_NAME]
        self.blocks = track_data.blocks 
        self.switches = track_data.switches # dictionaries don't require sorting duh
        self.lights = track_data.lights
        self.crossings = track_data.crossings

        self.controllers = [] # A collection of wayside has controllers
        self.CONTROLLER_COUNT = len(track_data.territory_counts) # get the number of controllers (CONSTANT)

        self.blocks = sorted(self.blocks, key=lambda block: (block.territory, block.id[0], int(block.id[1:]))) # sort blocks by territory then by section then by number

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
        
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.connect_signals()
                
        self.timer.start()

        
    
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
    
    @pyqtSlot()
    def update_track_model(self):
        """
        Sends the outputs of each controller's plc program upon the collection's timer timing outs
        """
        if self.track_model != None:
            switch_states = []
            light_states = []
            crossing_states = []
            temp_commanded_speeds = []
            temp_commanded_authorities = []
            commanded_speeds = {}
            commanded_authorities = {}
            maintenances = {}
            # loop through each controller to get values for entire track
            for controller in self.controllers:
                # LISTS
                switch_states = switch_states + controller.switch_positions
                light_states = light_states + controller.light_signals
                crossing_states = crossing_states + controller.crossing_signals

                # DICTIONARIES
                temp_commanded_speeds = temp_commanded_speeds + controller.commanded_speeds
                temp_commanded_authorities = temp_commanded_authorities + controller.commanded_authorities

            for i, block in enumerate(self.blocks):
                if temp_commanded_speeds[i] != None:
                    commanded_speeds[block.id] = temp_commanded_speeds[i]
                if temp_commanded_authorities[i] != None:
                    commanded_authorities[block.id] = temp_commanded_authorities[i]

            # send the outputs along with the sorted block struct so that they can interpret the values
            self.track_model.update_from_plc_outputs(self.blocks, switch_states, light_states, crossing_states)

            # call the update in the track model
            self.track_model.update_from_comms_outputs(wayside_speeds=commanded_speeds, wayside_authorities=commanded_authorities, maintenances=maintenances)

    @pyqtSlot()
    def update_ctc(self):
        """
        Called by the collection's timer so that the block occupancies, and plc outputs can be sent.
        """
        territory_sorted_occupancies = [] # get the entire tracks occupancies in one list sorted by territory

        for i, controller in enumerate(self.controllers): # for each controller append their occupancies
            territory_sorted_occupancies = territory_sorted_occupancies + controller.block_occupancies
        
        occupancies = {} # create a dictionary to match occupancy to it's block
        for i, block in enumerate(self.blocks):
            occupancies[block.id] = territory_sorted_occupancies[i] # match my lists values to their id
            
        signals.communication.wayside_block_occupancies.emit(occupancies) # send dictionary to ctc


    def update_block_occupancies(self, occupancies:dict):
        """
        Receives occupancy updates from the track model (called by the track model)

        :param occupancies: A dictionary of block occupancies with keyed with the block id
        """
        if self.track_model != None:
            sorted_occupancies = [] # create a list for the sorted occupancies to go in
            for block in self.blocks: # iterate through my sorted blocks (sorted by territory then block id)
                occupancy = occupancies.get(block.id, Occupancy.UNOCCUPIED) # read from the dictionary

                if occupancy == Occupancy.UNOCCUPIED:
                    self.sorted_occupancies.append(False)
                else:
                    self.sorted_occupancies.append(True)

            for i, controller in enumerate(self.controllers):
                controller.block_occupancies = sorted_occupancies[slice(*self.BLOCK_RANGES[i])] # goofy slice combined with unpacking operator but I like it

        

    @pyqtSlot(str, bool)
    def handle_switch_maintenance(self, block_id, position):
        """
        This function is called when the ctc makes a request to change a switch a position

        :param block_id: The id of the block with the switch

        :param position: The requested position to change the switch to
        """
    
    @pyqtSlot(list)
    def handle_exit_blocks(self, current_exit_blocks):
        """
        Called when the ctc sends what the exit blocks are. Does stuff for exit blocks?

        :param current_exit_blocks: A list of vectors per wayside controller indicating the active exit block
        """

    @pyqtSlot()
    def handle_dispatch(self):
        """
        Called when the ctc dispatches a train. Verifies that it is safe to dispatch the train
        """
        if self.track_model != None:
            if self.track_model.occupancies["K63"] == Occupancy.UNOCCUPIED:
                self.track_model.initialize_train()
        print("In collection handler for dispatch")
    @pyqtSlot(str, bool)
    def handle_block_maintenance(self, block_id, value):
        """
        Called when the ctc puts a block into maintenance

        :param block_id: the block id such as "A1":

        :param state:  0 for maintenance off, 1 for maintenance on
        """
        


    @pyqtSlot(dict,dict)
    def handle_suggested_values(self, speeds, authorities):
        """
        Called when the ctc sends suggested speeds and suggested authorities

        :param speeds: a dictionary of suggested speeds from the ctc that is keyed with the block id to the corresponding train 

        :param authorities: a list of suggested authoritities from the ctc that is key 
        """
        print("IN SUGGESTED VALUES")
        sorted_speeds = [] # converting the dictionaries sent by the ctc 
        sorted_authorities = [] # so that they match my ordering of the blocks by territory and are iterable lists
        # Need to get the suggested 
        for block_index, block in enumerate(self.blocks):
            speed = speeds.get(block.id, None) # default to None in the case that there is no value sent
            authority = authorities.get(block.id, None)
            
            controller_index = block.territory - 1 # find which controller this block is in
            relative_block_index = block_index + self.BLOCK_RANGES[controller_index][0] # find the relative block index to the controller
            
            if speed == None: # no value means just use the previous
                speed = self.controllers[controller_index].suggested_speeds[relative_block_index] # set the speed to its previous value since no change detected
            
            if authority == None: # no value means use the previous
                authority = self.controllers[controller_index].suggested_authorities[relative_block_index]

            if speed != None:
                speed = speed if speed <= block.speed_limit else 0 # basic clamp for speeds

            # put in lists for next loop that sends it to each backend controller
            sorted_speeds.append(speed)
            sorted_authorities.append(authority)


        # This loop calls a function in each controller individually
        for i, controller in enumerate(self.controllers):
            # set the controller suggested speeds and authorities
            controller.suggested_speeds = sorted_speeds[slice(*self.BLOCK_RANGES[i])]
            controller.suggested_authorities = sorted_authorities[slice(*self.BLOCK_RANGES[i])]
            

    def connect_signals(self): # may still need this when using signals later
        """
        Connects any necessary local and global signals for communication using the pyqt framework
        """
        signals.communication.ctc_switch_maintenance.connect(self.handle_switch_maintenance)
        signals.communication.ctc_exit_blocks.connect(self.handle_exit_blocks)
        signals.communication.ctc_dispatch.connect(self.handle_dispatch)
        signals.communication.ctc_block_maintenance.connect(self.handle_block_maintenance)
        signals.communication.ctc_suggested.connect(self.handle_suggested_values)
        self.timer.timeout.connect(self.update_track_model)
        self.timer.timeout.connect(self.update_ctc)


    #DEFINE A FUNCTION THAT EITHER GRABS VALUES FROM THE TRACK REFERENCE OR FROM THE TESTBENCH DEPENDING ON THE MODE OF THE CONTROLLER
    # FOR EACH CONTROLLER CHECK THE MODE 
    # READ EACH VALUE FROM TRACK MODEL EVERY UPDATE IF NOT IN MAINTENANCE MODE
    # OTHERWISE ONCE TESTBENCH WRITES A NEW VALUE TO THE WAYSIDE
    # WHEN EXITING RESET MAINTENANCE (DONE) RESET THE BACKEND VALUES (EASY) RESET THE TESTBENCH VALUES ( i guess choose whatever is easier?)
