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
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem, QFileDialog, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from track_constants import BLOCK_COUNT, SWITCH_COUNT, LIGHT_COUNT, CROSSING_COUNT, CONTROLLER_COUNT, EXIT_BLOCK_COUNT
from wayside_controller_ui import Ui_MainWindow as WaysideUi
from wayside_controller_testbench_ui import Ui_MainWindow as TestbenchUi

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class WaysideControllerFrontend(QMainWindow):
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class. Inherits from teh QMainWindow because ?
    """
    # signals below, if used should move to external file that all modules can reference?
    #open_testbench = pyqtSignal(str, int) # signal that opens a testbench with the name of the window
    #close_testbench = pyqtSignal(int) # signal that closes a testbench

    def __init__(self, collection_reference: WaysideControllerCollection):
        """
        :param collection_reference: Reference to the Wayside Collection object so that the UI can display the values in the backend
        """
        super().__init__()
        self.collection = collection_reference
        self.current_controller_index = 0 # Tells the ui which backend controller from the collection to reference
        self.ui = WaysideUi() # create a ui from the exported file
        self.ui.setupUi(self) 
        self.setWindowTitle("Wayside Controller Module")
       

        # Initialize any Ui elements that are dynamic
        self.init_table()
        self.init_combo_box()
        
         # Create a timer
        self.timer = QTimer(self)
        self.timer.setInterval(50)
        
        # Connect Signals to Slots
        self.ui.import_plc_button.clicked.connect(self.handle_input_program)
        self.ui.controller_select_combo_box.currentIndexChanged.connect(self.handle_controller_selection)
        self.ui.mode_select_combo_box.currentIndexChanged.connect(self.handle_mode_selection)
        self.timer.timeout.connect(self.update_ui)

        # read data from the collection to populate the combo box with num of controllers etc.
        # read data from the collection to generate rows in the table for blocks etc
        # read data from the currently indexed backend to show in the table
        self.timer.start()
    
    def init_combo_box(self):
        """
        Responsible for populating the combo box for selecting wayside controllers with the appropriate text
        """
        combo_box = self.ui.controller_select_combo_box
        for i in range(CONTROLLER_COUNT[self.collection.line_name]):
            controller_name = self.collection.line_name + " Line Controller #" + str(i + 1)
            combo_box.addItem(controller_name)

       
    
    def init_table(self):
        """
        Makes it so that the tables fit the screen appropriately. Also sets the number of rows to be in accordance with the current number of blocks
        """
        self.ui.block_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setup_table_dimensions(self.ui.block_table)


    def setup_table_dimensions(self, table: QTableWidget):
        """
        Used in table initialization, resizes the table to fit the desired space
        
        :param table: A QTableWidget
        """

        col_header = table.horizontalHeader()

        # Make all columns stretch equally
        for col in range(table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)
    
    def set_row_count(self, table: QTableWidget) -> bool:
        """
        Makes it so that the table row count matches the number of blocks in the corresponding wayside controller's territory

        :param table: A QTableWidget

        :return changed: If the row count has changed then this value will be True
        """

        if table.rowCount() < BLOCK_COUNT[self.collection.line_name][self.current_controller_index]: # if the current row count is less
            for row in range(table.rowCount(), BLOCK_COUNT[self.collection.line_name][self.current_controller_index]):
                # NEED TO INSET THE NAME OF THE ROW AS THE NAME OF THE BLOCK, HOW?? Talk to aaron and pj and pray they have a way already
                # THIS WAY OF DOING IT COULD BE BAD SINCE ROW NAMES NEED TO CHANGE REGARDLESS
                table.insertRow(row) # insert until row count is equivalent
            
            return True
        elif table.rowCount() > BLOCK_COUNT[self.collection.line_name][self.current_controller_index]:
            for row in range(BLOCK_COUNT[self.collection.line_name][self.current_controller_index], table.rowCount()):
                table.removeRow(row) # remove until row count is equivalent
            
            return True
        return False
    
    def populate_table(self, table: QTableWidget):
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
            row = 0
            for value in data[col]: 
                if value != None: # Skip items that don't need to be written
                    item = QTableWidgetItem() # Create an item to go in the table
                    unit = " yards" if col % 2 == 0 else " mph" # Figure out what the unit should be depending on the position in the table
                    if type(value) is float or type(value) is int: # If the column has a numeric value it should have a unit attatched
                        text = str(value) + unit
                    elif type(value) is bool: # For bools the text should say occupied/unoccupied since only bool in table is occupancy
                        text = "Occupied" if value else "Unoccupied"
                    item.setText(text) # set the items text attribute
                    table.setItem(row, col, item) # put the item in the table
                row += 1
    
    def populate_list(self, q_list: QListWidget):
        """
        Adds entries to the input list. Runs every ui update that the controller has switched.

        :param list: A pyqt QListWidget
        """
        q_list.clear()
        list_name = q_list.objectName()
        active_controller = self.collection.controllers[self.current_controller_index]

        if list_name == "switch_list":
            row_count = SWITCH_COUNT[self.collection.line_name][self.current_controller_index]
            for i in range(row_count):
                if active_controller.switch_positions[i] != None:
                    item = QListWidgetItem()
                    text = "Switch " + str(i + 1) # FOR NOW, WILL NEED TO FIGURE OUT HOW TO GET THE SPECIFIC LABEL
                    item.setText(text)
                    q_list.addItem(item)
        elif list_name == "light_list":
            row_count = LIGHT_COUNT[self.collection.line_name][self.current_controller_index]
            for i in range(row_count):
                if active_controller.light_signals[i] != None:
                    item = QListWidgetItem()
                    text = "Light " + str(i + 1) # FOR NOW, WILL NEED TO FIGURE OUT HOW TO GET THE SPECIFIC LABEL
                    item.setText(text)
                    q_list.addItem(item)
        elif list_name == "crossing_list":
            row_count = CROSSING_COUNT[self.collection.line_name][self.current_controller_index]
            for i in range(row_count):
                if active_controller.crossing_signals[i] != None:
                    item = QListWidgetItem()
                    text = "Crossing " + str(i + 1) # FOR NOW, WILL NEED TO FIGURE OUT HOW TO GET THE SPECIFIC LABEL
                    item.setText(text)
                    q_list.addItem(item)
        else:
            raise ValueError(f"Invalid Input. QListWidget Does not match any in the UI.")
    
    def show_current_selected_output(self, q_list: QListWidget, label: QLabel):
        """
        Updates the corresponding label on the ui with the output of the list item that is selected

        :param q_list: A QListWidget, the currently selected item's value will be output on the screen

        :param label: A QLabel corresponding to the list, will update to have the output of the selected item
        """
        active_controller = self.collection.controllers[self.current_controller_index]

        list_name = q_list.objectName()
        label_name = label.objectName()
    
        index = q_list.currentRow()
        current_item = q_list.currentItem()

        if index >= 0 and current_item != None:
            if list_name == "switch_list" and label_name == "switch_label":
                item_name = current_item.text() 
                value = "Up" if active_controller.switch_positions[index] else "Down"
                label.setText(item_name + ": " + value)
            elif list_name == "light_list" and label_name == "light_label":
                item_name = current_item.text()
                value = "Green" if active_controller.light_signals[index] else "Red"
                label.setText(item_name + ": " + value)
            elif list_name == "crossing_list" and label_name == "crossing_label":
                item_name = current_item.text()
                value = "Active" if active_controller.crossing_signals[index] else "Inactive"
                label.setText(item_name + ": " + value)
            else:
                raise ValueError(f"Invalid Input: Make sure the input list and label correspond.")
        else:
            if list_name == "switch_list" and label_name == "switch_label":
                text = "Switch: Not Selected"
                label.setText(text)
            elif list_name == "light_list" and label_name == "light_label":
                text = "Light: Not Selected"
                label.setText(text)
            elif list_name == "crossing_list" and label_name == "crossing_label":
                text = "Crossing: Not Selected"
                value = "Active" if active_controller.crossing_signals[index] else "Inactive"
                label.setText(text)
            else:
                raise ValueError(f"Invalid Input: Make sure the input list and label correspond.")



    def closeEvent(self, event):
        """
        Overridden Mainwindow function that handles when the user clicks the exit button in the corner of the window
        """
        for testbench in self.collection.testbenches: # Close every testbench that is active as well
            testbench.close() 
        event.accept()



    @pyqtSlot()
    def update_ui(self):
        """
        Timer based update to read values from the backend and display them in the frontend
        """
        active_controller = self.collection.controllers[self.current_controller_index] # Figure out the current controller
        
        self.ui.current_filename_label.setText("Current Filename: " + active_controller.plc_filename)  # update the ui to show the file imported for the plc
        self.ui.mode_select_combo_box.setCurrentIndex(1 if active_controller.maintenance_mode else 0) # Check to make sure the correct mode is displayed
        
        
        controller_changed = self.set_row_count(self.ui.block_table) # performs a check to see if the rows changed in the table ie the controller changed

        if controller_changed: # Perform any ui updates that only happen when the controller changes
            self.ui.menu_bar.setTitle(self.ui.controller_select_combo_box.currentText())
            self.populate_list(self.ui.switch_list)
            self.populate_list(self.ui.light_list)
            self.populate_list(self.ui.crossing_list)
        
        self.populate_table(self.ui.block_table) # populate the table with values from the backend regardless, but only after the rows have been updated
        
        self.show_current_selected_output(self.ui.switch_list, self.ui.switch_label)
        self.show_current_selected_output(self.ui.light_list, self.ui.light_label)
        self.show_current_selected_output(self.ui.crossing_list, self.ui.crossing_label)



        # SHOULD PROB HANDLE SOME OF THOSE EXCEPTIONS HUH
  


    @pyqtSlot(int)
    def handle_controller_selection(self, controller_index):
        """
        Called to updates the UI when the combo box specifying the current wayside controller changes.

        :param index: The index sent from the controller select combo box
        """
        if controller_index != self.current_controller_index: # only change it if it changes? not really sure this line is needed alas safety first
            self.current_controller_index = controller_index
            
            

    @pyqtSlot(int)
    def handle_mode_selection(self, mode_index): 
        """
        Called to open a window to allow the programmer to input test values when the mode changes from auto -> maintenance

        :param index: The index sent by the mode selection combo box
        """
        # Make some temporary variables in this scope to help with reading
        active_controller = self.collection.controllers[self.current_controller_index]

        # Check if the mode was changed to maintenance mode
        if mode_index == 1 and not active_controller.maintenance_mode: # changing mode from auto to maintenance
            # Perform a check to see if there exists a block in the territory that is occupied
            for block in active_controller.block_occupancies:
                if block == True:
                    self.ui.mode_select_combo_box.setCurrentIndex(0) # reset the combo box back to automatic to signal it could not be changed
                    return # exit early to avoid opening the manual input window
            
            # SOMEHOW SWITCH TO READING THE VALUES FROM THE TESTBENCH
            testbench_window_name = self.ui.menu_bar.title() + " Testbench"
            active_testbench = self.collection.testbenches[self.current_controller_index]
            active_testbench.open_window(testbench_window_name)
            active_controller.maintenance_mode = True
             # Set the exit blocks to be occupied and open the test bench window 
             # Open the test bench window probably other stuff todo as well but whale i cant think of it
          
        # Check if the mode was changed to automatic mode
        elif mode_index == 0 and active_controller.maintenance_mode: # changing mode from maintenance to auto
            #self.close_testbench.emit() # close the window
            active_testbench = self.collection.testbenches[self.current_controller_index]
            active_testbench.hide_window()
            active_controller.maintenance_mode = False
            # SWITCH BACK TO READING THE VALUES from other modules?
            # close the testbench window

    @pyqtSlot()
    def handle_input_program(self):
        """
        Called when the programmer clicks the input program button. 
        """
        active_controller = self.collection.controllers[self.current_controller_index] # get the actively showing controller

        while True:
            program_file_path, _ = QFileDialog.getOpenFileName(self, "Select PLC Program", "", "Python File (*.py);;All Files (*)") # something i don't fully understand
            if program_file_path:
                if active_controller.load_program(program_file_path): # returns true if valid plc program
                    active_controller.plc_filename = Path(program_file_path).name # store the filename in the backend
                    break
            else:
                break
                
class WaysideControllerTestbench(QMainWindow):
    def __init__(self, collection_reference: WaysideControllerCollection, idx: int):
        """
        :param collection_reference: A reference to the wayside controller collection that the testbench is a part of
        :param idx: The index that matches the testbench to the backend controller
        """
        super().__init__()
        self.test_ui = TestbenchUi() # create a ui from the exported file
        self.test_ui.setupUi(self) 
        self.collection = collection_reference
        self.index = idx
        # populate the ui with the backend stuff somehow?
    
    
    def open_window(self, window_name: str):
        """
        opens the testbench window when the user switches to maintenance mode

        :param window_name: The title of the menu? window
        """
        self.setWindowTitle("Wayside Testbench Module")
        self.test_ui.menu_Blue_Line_Controller_1.setTitle(window_name)
        self.show()
    
    def hide_window(self): 
        """
        My defined function for hiding the testbench window when the user exits maintenance mode via the combo box on the ui
        """
        # just gonna leave the window in the previous state it was in if it ever is reopened
        # can add more here if there needs to be any handling of exiting the testbench since its called in both teh closeEvent and from the frontend main window
       
        self.hide()
    
    def closeEvent(self, event):
        """
        Overridden Mainwindow function that handles when the user clicks the exit button in the corner of the window
        """
        self.collection.controllers[self.index].maintenance_mode = False # User has closed the window so maintenance mode should no longer be active
        self.hide_window()
        event.ignore() # do not let the user actually destroy the window



if __name__ == "__main__":
    app = QApplication(sys.argv)
    collection = WaysideControllerCollection("GREEN")
    collection.frontend.show()
    sys.exit(app.exec_())