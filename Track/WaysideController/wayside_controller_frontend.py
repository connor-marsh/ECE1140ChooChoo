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
from track_constants import BLOCK_COUNT, SWITCH_COUNT, LIGHT_COUNT, CROSSING_COUNT, CONTROLLER_COUNT, EXIT_BLOCK_COUNT
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
        self.init_combo_box()
        

        # read data from the collection to populate the combo box with num of controllers etc.
        # read data from the collection to generate rows in the table for blocks etc
        # read data from the currently indexed backend to show in the table
    
    def init_combo_box(self):
        """
        Responsible for populating the combo box for selecting wayside controllers with the appropriate text
        """
        combo_box = self.ui.controller_select_combo_box
        for i in range(CONTROLLER_COUNT[self.collection.line_name]):
            controller_name = self.collection.line_name + " Line Controller #" + str(i + 1)
            combo_box.addItem(controller_name)

        self.ui.menu_bar.setTitle(combo_box.currentText())
    
    def init_tables(self):
        """
        Makes it so that the tables fit the screen appropriately. Also sets the number of rows to be in accordance with the current number of blocks
        """
        self.setup_table_dimensions(self.ui.block_table)
        self.setup_table_dimensions(self.ui.junction_table)
        self.set_row_count(self.ui.block_table)
        self.set_row_count(self.ui.junction_table)

    def setup_table_dimensions(self, table):
        """
        Used in table initialization, resizes the table to fit the desired space
        
        :param table: A QTableWidget
        """

        col_header = table.horizontalHeader()

        # Make all columns stretch equally
        for col in range(table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)
    
    def set_row_count(self, table):
        """
        Makes it so that the table row count matches the number of blocks in the corresponding wayside controller's territory

        :param table: A QTableWidget
        """
        table.clearContents() # Reset the contents of the table so that new ones can be written later

       
        if table.rowCount() < BLOCK_COUNT[self.collection.line_name][self.current_controller]: # if the current row count is less
            # For each row that needs to be added
            for row in range(table.rowCount(), BLOCK_COUNT[self.collection.line_name][self.current_controller], 1):
                table.insertRow(row) # insert until row count is equivalent
        else:
            for row in range(table.rowCount(), BLOCK_COUNT[self.collection.line_name][self.current_controller], -1):   
                table.removeRow(row) # remove until row count is equivalent
        

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
    wayside_window.setWindowTitle("Wayside Controller Module")
    wayside_window.show()
    sys.exit(app.exec_())