"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that implements any necessary logic for the Wayside Controller UI 
"""
import sys
import os
from pathlib import Path
from wayside_controller_collection import WaysideControllerCollection
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from track_constants import BLOCK_COUNT, SWITCH_COUNT, LIGHT_COUNT, CROSSING_COUNT, CONTROLLER_COUNT, EXIT_BLOCK_COUNT
from wayside_controller_ui import Ui_MainWindow as WaysideUi
from wayside_controller_testbench_ui import Ui_MainWindow as TestbenchUi

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
        self.current_controller_index = 0 # Tells the ui which backend controller from the collection to reference
        self.ui = WaysideUi() # create a ui from the exported file
        self.ui.setupUi(self) 
        
        

        # Initialize any Ui elements that are dynamic
        self.init_tables_lists()
        self.init_combo_box()
        
        # Create a timer
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.start()
        
        # Connect Signals to Slots
        self.ui.import_plc_button.clicked.connect(self.handle_input_program)
        self.ui.controller_select_combo_box.currentIndexChanged.connect(self.handle_controller_selection)
        self.ui.mode_select_combo_box.currentIndexChanged.connect(self.handle_mode_selection)
        self.timer.timeout.connect(self.update_ui)

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
    
    def init_tables_lists(self):
        """
        Makes it so that the tables fit the screen appropriately. Also sets the number of rows to be in accordance with the current number of blocks
        """
        self.setup_table_dimensions(self.ui.block_table)
        self.set_row_count(self.ui.block_table)


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

        if table.rowCount() < BLOCK_COUNT[self.collection.line_name][self.current_controller_index]: # if the current row count is less
            for row in range(table.rowCount(), BLOCK_COUNT[self.collection.line_name][self.current_controller_index]):
                table.insertRow(row) # insert until row count is equivalent
        elif table.rowCount() > BLOCK_COUNT[self.collection.line_name][self.current_controller_index]:
            for row in range(BLOCK_COUNT[self.collection.line_name][self.current_controller_index], table.rowCount()):
                table.removeRow(row) # remove until row count is equivalent
    
    def populate_table(self, table):
        """
        Writes the latest values from the currently selected backend to the table

        :param table: A QTableWidget
        """
        active_controller = self.collection.controllers[self.current_controller_index] # Figure out the current controller

        # Get an iterable form of the data that looks like the table
        # This is probably a bad and stupid way to do this
        
        data = [active_controller.block_occupancies, 
                active_controller.suggested_speeds,  # The rest of the values are simply floats that can just be 
                active_controller.suggested_authorities,
                active_controller.commanded_speeds,
                active_controller.commanded_authorities]
        
        for col in range(table.columnCount()): # Each Column in the table is one of the lists in the matrix above
            for row in range(table.rowCount()): # Each row is an item in the lists
                if data[col][row] != None: # Skip rows that don't need to be written
                    item = QTableWidgetItem() # Create an item to go in the table
                    unit = " yards" if col % 2 == 0 else " mph" # Figure out what the unit should be depending on the position in the table
                    if type(data[col][row]) is float or type(data[col][row]) is int: # If the column has a numeric value it should have a unit attatched
                        text = str(data[col][row]) + unit
                    elif type(data[col][row]) is bool: # For bools the text should say occupied/unoccupied since only bool in table is occupancy
                        text = "Occupied" if data[col][row] else "Unoccupied"
                    item.setText(text) # set the items text attribute
                    table.setItem(row, col, item) # put the item in the table


    @pyqtSlot()
    def update_ui(self):
        """
        Timer based update to read values from the backend and display them in the frontend
        """
        active_controller = self.collection.controllers[self.current_controller_index] # Figure out the current controller

        # Update every ui element
        self.set_row_count(self.ui.block_table)
        self.ui.current_filename_label.setText("Current File: " + active_controller.plc_filename) # update the current filename on screen
        self.ui.menu_bar.setTitle(self.ui.controller_select_combo_box.currentText())
        self.populate_table(self.ui.block_table)
        #self.set_row_count(self.ui.junction_table)
        # make several lists, Switch pos. | Lights | Crossings
        # then update functions for those

    @pyqtSlot(int)
    def handle_controller_selection(self, index):
        """
        Called to updates the UI when the combo box specifying the current wayside controller changes.

        :param index: The index sent from the controller select combo box
        """
        if index != self.current_controller_index:
            self.current_controller_index = index
            
        # make sure to update the menu label
        # make sure to update the row count of the tables
        # make sure to set the mode combo box to be the correct mode?

    @pyqtSlot(int)
    def handle_mode_selection(self, index): # maybe do not allow the user to change the active controller when in manual mode?
        """
        Called to open a window to allow the programmer to input test values when the mode changes from auto -> maintenance

        :param index: The index sent by the mode selection combo box
        """
        # Make some temporary variables in this scope to help with reading
        active_controller = self.collection.controllers[index]

        # Check if the mode was changed, otherwise do nothing
        if self.ui.mode_select_combo_box.currentIndex() == 1 and not active_controller.maintenance_mode: # changing mode from auto to maintenance
            # Perform a check to see if there exists a block in the territory that is occupied
            for block in active_controller.block_occupancies:
                if block == True:
                    self.ui.mode_select_combo_box.setCurrentIndex(0) # reset the combo box back to automatic to signal it could not be changed
                    return # exit early to avoid opening the manual input window
            
            # SOMEHOW SWITCH TO READING THE VALUES FROM THE TESTBENCH
             # Set the exit blocks to be occupied and open the test bench window 
             # Open the test bench window probably other stuff todo as well but whale i cant think of it
            active_controller.maintenance_mode = True # No occupied blocks detected can safely set the active mode to maintenance
        elif self.ui.mode_select_combo_box.currentIndex() == 0 and active_controller.maintenance_mode: # changing mode from maintenance to auto
            active_controller.maintenance_mode = False

            # SWITCH BACK TO READING THE VALUES FROM THE 
            # close the testbench window

    @pyqtSlot()
    def handle_input_program(self):
        """
        Called when the programmer clicks the input program button. 
        """
        active_controller = self.collection.controllers[self.current_controller_index]

        while True:
            program_file_path, _ = QFileDialog.getOpenFileName(self, "Select PLC Program", "", "Python File (*.py);;All Files (*)")
            if program_file_path:
                if active_controller.load_program(program_file_path):
                    active_controller.plc_filename = Path(program_file_path).name # store the filename in the backend
                    break
            else:
                break
                



if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = WaysideControllerCollection("GREEN")
    wayside_window = collection.frontend
    wayside_window.setWindowTitle("Wayside Controller Module")
    wayside_window.show()
    sys.exit(app.exec_())