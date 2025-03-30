"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that contains several WaysideControllers and a Frontend. Responsible for interfacing with the Track Model and CTC
"""
import sys
from track_constants import BLOCK_COUNT, SWITCH_COUNT, LIGHT_COUNT, CROSSING_COUNT, CONTROLLER_COUNT, EXIT_BLOCK_COUNT, TRACK_NAMES
from wayside_controller_backend import WaysideController
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt

class WaysideControllerCollection():
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class.
    """

    def __init__(self, line_name="GREEN"):
        """
        :param line_name: Selects controller count etc. depending on the line. Either "RED" or "GREEN"
        """
        
        if line_name not in TRACK_NAMES:
            raise ValueError(f"Invalid input. Please enter exactly the line name of an existing track.")
        
        self.line_name = line_name # Keep the line name as a member variable

        # Create a list of backends which will handle different territory, devices, etc.
        self.controllers = [WaysideController(BLOCK_COUNT[line_name][i], SWITCH_COUNT[line_name][i], 
                                                          LIGHT_COUNT[line_name][i], CROSSING_COUNT[line_name][i], EXIT_BLOCK_COUNT[line_name][i], 0.5)
                                                          for i in range(CONTROLLER_COUNT[line_name])]

        
        # Create a list of testbenches for maintenance mode corresponding to each one of the wayside controllers
        from wayside_controller_frontend import WaysideControllerTestbench # Avoiding circular imports?
        self.testbenches = [WaysideControllerTestbench(self, i) for i in range(CONTROLLER_COUNT[line_name])]

       
        # Initialize the frontend with access to the collection so that it may modify itself or the backend using the data from the backend
        from wayside_controller_frontend import WaysideControllerFrontend # lazy import to avoid circular import (do NOT tell me about design patterns)
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = WaysideControllerCollection("GREEN")
    collection.frontend.show()
    sys.exit(app.exec_())
