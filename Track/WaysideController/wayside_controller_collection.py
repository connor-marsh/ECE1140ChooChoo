"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that contains several WaysideControllers and a Frontend. Responsible for interfacing with the Track Model and CTC
"""
import sys
from track_constants import BLOCK_COUNT, SWITCH_COUNT, LIGHT_COUNT, CROSSING_COUNT, CONTROLLER_COUNT, EXIT_BLOCK_COUNT
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
        
        self.line_name = line_name # Keep the line name as a member variable

        # Create a list of backends which will handle different territory, devices, etc.
        self.controllers = [None] * CONTROLLER_COUNT[line_name]
        for i in range(CONTROLLER_COUNT[line_name]):
            self.controllers[i] = WaysideController(0.5, BLOCK_COUNT[line_name][i], SWITCH_COUNT[line_name][i], 
                                                          LIGHT_COUNT[line_name][i], CROSSING_COUNT[line_name][i], EXIT_BLOCK_COUNT[line_name][i])
       
        # Initialize the frontend with access to the collection so that it may modify itself or the backend using the data from the backend
        from wayside_controller_frontend import WaysideControllerFrontend # lazy import to avoid circular import (do NOT tell me about design patterns)
        self.frontend = WaysideControllerFrontend(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = WaysideControllerCollection("GREEN")
    collection.frontend.show()
    sys.exit(app.exec_())
