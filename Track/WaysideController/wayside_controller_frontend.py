"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that implements any necessary logic for the Wayside Controller UI 
"""
import sys
import os
from wayside_controller_collection import WaysideControllerCollection
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from wayside_controller_ui import Ui_MainWindow

class WaysideControllerFrontend(QMainWindow):
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class. Inherits from teh QMainWindow because ?
    """

    def __init__(self, collection_reference: WaysideControllerCollection):
        """
        :param collection_reference: Reference to the Wayside Collection object so that the UI can display the values in the backend
        """
        super().__init__()
        self.collection = collection_reference
        self.current_controller = 0 # Tells the ui which backend controller from the collection to reference
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.init_tables()

        # example code for changing the window name, put in the update function for the ui.
        #self.ui.menuWayside_Controller_Blue_Line_1.setTitle(self.ui.section_select_combo_box.currentText())

        # read data from the collection to populate the combo box with num of controllers etc.
        # read data from the collection to generate rows in the table for blocks etc
        # read data from the currently indexed backend to show in the table
    
    def init_combo_box(self):
        """
        Responsible for populating the combo box for selecting wayside controllers with the appropriate text
        """
    
    def init_tables(self):
        """
        Sets it so that the tables fit the screen appropriately. Sets the number of rows and names them
        """
        self.setup_table_dimension(self.ui.block_table)
        self.setup_table_dimensions(self.ui.junction_table)

    def setup_table_dimensions(self, table):
        """
        Used in table initialization, resizes the table to fit the desired space
        
        :param table: A QTableWidget
        """

        col_header = table.horizontalHeader()

        # Make all columns stretch equally
        for col in range(table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)

    def update_ui(self):
        """
        Timer based update to read values from the backend and display them in the frontend
        """
    
    def handle_controller_selection(self):
        """
        Called to updates the UI when the combo box specifying the current wayside controller changes. 
        """

    def handle_mode_selection(self):
        """
        Called to open a window to allow the programmer to input test values when the mode changes from auto -> maintenance
        """

    def handle_input_program(self):
        """
        Called when the programmer clicks the input program button. 
        """
if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = WaysideControllerCollection("GREEN")
    wayside_window = WaysideControllerFrontend(collection)
    wayside_window.show()
    sys.exit(app.exec_())