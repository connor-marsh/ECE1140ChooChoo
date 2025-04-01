"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that contains several WaysideControllers and a Frontend. Responsible for interfacing with the Track Model and CTC
"""
import sys
import globals.track_data_class as track_data
from Track.WaysideController.wayside_controller_backend import WaysideController
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

class WaysideControllerCollection():
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class.
    """
    def __init__(self, track_data=track_data.TrackDataClass):
        """
        :param track_data: A class that contains the unchanging data imported from the track builder
        """
    
        
        self.LINE_NAME = track_data.line_name
        self.controllers = [] # A collection of wayside has controllers
        self.CONTROLLER_COUNT = len(track_data.territory_counts) # get the number of controllers (CONSTANTS)
        print(self.CONTROLLER_COUNT)
        # Will get the number of each below (CONSTANTS)
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
                                                      light_count=light_count,crossing_count=crossing_count,exit_block_count=0,scan_time=0.5))

        print(self.BLOCKS_COUNTS)
        # Create a list of testbenches for maintenance mode corresponding to each one of the wayside controllers
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerTestbench # Avoiding circular imports?
        self.testbenches = [WaysideControllerTestbench(self, i) for i in range(self.CONTROLLER_COUNT)]

       
        # Initialize the frontend with access to the collection so that it may modify itself or the backend using the data from the backend
        from Track.WaysideController.wayside_controller_frontend import WaysideControllerFrontend # lazy import to avoid circular import (do NOT tell me about design patterns)
        self.frontend = WaysideControllerFrontend(self)

        #self.connect_signals()

    def get_plc_outputs(self, controller_index : int) -> tuple[list[bool], list[bool], list[bool]]:
        """
        This function returns a tuple containing 3 lists of booleans containing the switch postions, light signals, crossing signals

        :param controller_index: The index to the controller 

        :return plc_outputs: tuple containing 3 lists of booleans containing each of the corresponding outputs of the select controller's plc
        """
        if controller_index < len(self.controllers) and controller_index >= 0: # check to see that the controller exists
            controller = self.controllers[controller_index]
            switches = self.controller.switch_positions
            lights = self.controller.light_signals
            crossings = self.controller.crossing_signals
            return (switches,lights,crossings) # TRIPLE REDUNDANCY?
        else:
            raise IndexError(f"The input index to the Wayside Controller is not in range")


    def get_wayside_commanded(self, controller_index : int) -> tuple[list[float], list[float]]:
        """
        This function returns a tuple containing 2 lists of floats, Commanded Authority and Commanded Speed

        :param controller_index: The index to the controller 

        :return commanded_values: Tuple containing 2 lists of booleans for each of the corresponding outputs of the select controller's plc
        """
        if controller_index < len(self.controllers) and controller_index >= 0: # check to see that the controller exists
            controller = self.controllers[controller_index]
            authorities = self.controller.commanded_authorities
            speeds = self.controller.commanded_speeds
            return (authorities, speeds) # TRIPLE REDUNDANCY?
        else:
            raise IndexError(f"The input index to the Wayside Controller is not in range")

    #DEFINE A FUNCTION THAT EITHER GRABS VALUES FROM THE TRACK REFERENCE OR FROM THE TESTBENCH DEPENDING ON THE MODE OF THE CONTROLLER
    # FOR EACH CONTROLLER CHECK THE MODE 
    # READ EACH VALUE FROM TRACK MODEL EVERY UPDATE IF NOT IN MAINTENANCE MODE
    # OTHERWISE ONCE TESTBENCH WRITES A NEW VALUE TO THE WAYSIDE
    # WHEN EXITING RESET MAINTENANCE (DONE) RESET THE BACKEND VALUES (EASY) RESET THE TESTBENCH VALUES ( i guess choose whatever is easier?)

    
    
    #def connect_signals(self): # may still need this when using signals later
    #    """
    #    Connects any necessary signals for communication using the pyqt framework
    #    """
    #    for testbench in self.testbenches

        #self.frontend.open_testbench.connect(self.testbench.open_window)
        #self.frontend.close_testbench.connect(self.testbench.close_window)
