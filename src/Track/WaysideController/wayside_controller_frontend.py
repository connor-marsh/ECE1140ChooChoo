"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    A Class that implements any necessary logic for the Wayside Controller UI 
"""
import sys
import os
from pathlib import Path
from Track.WaysideController.wayside_controller_collection import WaysideControllerCollection
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem, QFileDialog, QListWidget, QListWidgetItem, QLabel 
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QTimer
from Track.WaysideController.wayside_controller_ui import Ui_MainWindow as WaysideUi
from Track.WaysideController.wayside_controller_testbench_ui import Ui_MainWindow as TestbenchUi


os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class WaysideControllerFrontend(QMainWindow):
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class. Inherits from teh QMainWindow because ?
    """


    def __init__(self, collection_reference: WaysideControllerCollection, auto_import_programs=False):
        """
        :param collection_reference: Reference to the Wayside Collection object so that the UI can display the values in the backend
        :param auto_import_programs: Set true if you would like to automatically upload 3 green line plc programs automatically
        """

        super().__init__()
        self.collection = collection_reference
        self.current_controller_index = 0 # Tells the ui which backend controller from the collection to reference
        self.current_range = None # Tells the ui which range of blocks to display (initial value should guarantee that the update runs to change the table row count)
        self.ui = WaysideUi() # create a ui from the exported file
        self.ui.setupUi(self) 
        self.setWindowTitle("Wayside Controller Module")
       

        # Initialize any Ui elements that are dynamic
        self.init_table()
        self.init_combo_box()
        
         # Create a timer
        self.timer = QTimer(self)
        self.timer.setInterval(250) # Below 50ms and weird stuff happens since i prob wrote my update weird
        
        # Connect Signals to Slots
        self.ui.import_plc_button.clicked.connect(self.handle_input_program)
        self.ui.controller_select_combo_box.currentIndexChanged.connect(self.handle_controller_selection)
        self.ui.mode_select_combo_box.currentIndexChanged.connect(self.handle_mode_selection)
        self.timer.timeout.connect(self.update_ui)

        # read data from the collection to populate the combo box with num of controllers etc.
        # read data from the collection to generate rows in the table for blocks etc
        # read data from the currently indexed backend to show in the table

        if(auto_import_programs): # auto import the programs if necessary
            for i in range(3):
                # i sure hope these filepaths exists
                
                filepath = "src\Track\WaysideController\PLC\green_line_plc_" + str(i+1) + ".py"
                self.auto_get_program(i,filepath)

        self.timer.start()
    
    def init_combo_box(self):
        """
        Responsible for populating the combo box for selecting wayside controllers with the appropriate text
        """
        combo_box = self.ui.controller_select_combo_box
        for i in range(self.collection.CONTROLLER_COUNT):
            controller_name = self.collection.LINE_NAME + " Line Controller #" + str(i + 1)
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

        if self.current_range != self.collection.BLOCK_RANGES[self.current_controller_index]: # check to see if the controller changed
            self.current_range = self.collection.BLOCK_RANGES[self.current_controller_index] # update the range to match the current controller
            table.setRowCount(self.collection.BLOCK_COUNTS[self.current_controller_index]) # update the row count of the table
            for i in range(*self.current_range): # * is the unpacking operator, it unpacks the tuple so that the 0th entry is the lower bound and the 1st entry is the upper
                row = 0 + i - self.current_range[0] # The range of the blocks that is referenced does not match the indexing to the rows
                text = self.collection.blocks[i].id # want to use the block id as the label for the row
                if table.verticalHeaderItem(row) != None: # check to see if it exists
                    table.verticalHeaderItem(row).setText(text) # can just set the text of the current item
                else: # it does in fact exist
                    header_item = QTableWidgetItem(text) # otherwise create new item with text
                    table.setVerticalHeaderItem(row, header_item)
            return True # The controller displayed changed
        else:
            return False # The controller displayed did not change

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
    
    def populate_lists(self):
        """
        Adds entries to the input list. Runs every ui update that the controller has switched.
        """
        self.ui.switch_list.clear()
        self.ui.light_list.clear()
        self.ui.crossing_list.clear()
        
        for i in range(*self.current_range):
            block = self.collection.blocks[i]
            if block.switch: # if the block has a switch (I BELIEVE THESE ARE MUTUALLY EXCLUSIVE)
                text = "Switch " + block.id
                item = QListWidgetItem(text)
                self.ui.switch_list.addItem(item)
            if block.light: # if the block has a light
                text = "Light " + block.id
                item = QListWidgetItem(text)
                self.ui.light_list.addItem(item)
            if block.crossing: # if the block has a crossing
                text = "Crossing " + block.id
                item = QListWidgetItem(text)
                self.ui.crossing_list.addItem(item)

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
                id = item_name[7:] # extract the block id from the text
                value = self.collection.switches[id].positions[1] if active_controller.switch_positions[index] else self.collection.switches[id].positions[0] # reference the dictionary since specific to the switch
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
            self.populate_lists()
        
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
             # Set the exit blocks to be occupied and open the test bench window 
             # Open the test bench window probably other stuff todo as well but whale i cant think of it
          
        # Check if the mode was changed to automatic mode
        elif mode_index == 0 and active_controller.maintenance_mode: # changing mode from maintenance to auto
            #self.close_testbench.emit() # close the window
            active_testbench = self.collection.testbenches[self.current_controller_index]
            active_testbench.hide_window()
            
            # SWITCH BACK TO READING THE VALUES from other modules?
            # close the testbench window

    @pyqtSlot()
    def handle_input_program(self):
        """
        Called when the programmer clicks the input program button. 
        """
        active_controller = self.collection.controllers[self.current_controller_index] # get the actively showing controller
        while True:
            program_file_path, _ = QFileDialog.getOpenFileName(self, "Select PLC Program", "", "Python File (*.py)") # something i don't fully understand
            if program_file_path:
                if active_controller.load_program(program_file_path): # returns true if valid plc program
                    active_controller.plc_filename = Path(program_file_path).name # store the filename in the backend
                    break
            else:
                break


    def auto_get_program(self, controller_index, filepath):
        """
        Used when the plc programs are automatically imported

        :controller_index: which controller should the program run on

        :filepath: the filepath to the program:
        """
        active_controller = self.collection.controllers[controller_index]
        active_controller.load_program(filepath)
        active_controller.plc_filename = Path(filepath).name
        
            



class WaysideControllerTestbench(QMainWindow):
    def __init__(self, collection_reference: WaysideControllerCollection, idx: int):
        """
        :param collection_reference: A reference to the wayside controller collection that the testbench is a part of
        :param idx: The index that matches the testbench to the backend controller
        """
        super().__init__()
        self.ui = TestbenchUi() # create a ui from the exported file
        self.ui.setupUi(self) 
        self.collection = collection_reference
        self.controller_index = idx # never changes
        self.current_block_index = None # local to this testbench current block is the block clicked on the list
        self.first_open = True # Used to check to see if the testbench has been open before
        self.block_range = self.collection.BLOCK_RANGES[idx] # this never changes

        # Uncomment this loop to correspond the range to the relative index (writing plc programs)
        #print(self.controller_index)
        #relative_index = 0
        #for absolute_index in range(*self.block_range):
        #    print(self.collection.blocks[absolute_index].id, absolute_index, relative_index, relative_index + 1)
        #    relative_index += 1


        # Used for storing the values input by the user
        self.block_occupancies =     [None] * self.collection.BLOCK_COUNTS[idx]
        self.suggested_authorities = [None] * self.collection.BLOCK_COUNTS[idx] 
        self.suggested_speeds =      [None] * self.collection.BLOCK_COUNTS[idx]
        self.switch_positions =      [None] * self.collection.BLOCK_COUNTS[idx]
        self.light_signals =         [None] * self.collection.BLOCK_COUNTS[idx]
        self.crossing_signals =      [None] * self.collection.BLOCK_COUNTS[idx]

        # Connecting the list signals to the slot
        self.ui.select_block_list.itemClicked.connect(self.handle_block_selection) 
        self.ui.block_occupancy_confirm_button.clicked.connect(self.handle_occupancy_confirmation)
        self.ui.suggested_speed_confirm_button.clicked.connect(self.handle_speed_confirmation)
        self.ui.suggested_authority_confirm_button.clicked.connect(self.handle_authority_confirmation)
        self.ui.switch_position_confirm_button.clicked.connect(self.handle_switch_confirmation)
        self.ui.light_signal_confirm_button.clicked.connect(self.handle_light_confirmation)
        self.ui.crossing_signal_confirm_button.clicked.connect(self.handle_crossing_confirmation)


    @pyqtSlot()
    def handle_block_selection(self):
        """
        Called when the a new item is clicked, handles updating the ui elements
        """
        self.current_block_index = self.ui.select_block_list.currentRow() # get the current block by checking which item is clicked

        # Update the suggested speed fields to match the corresponding blocks user input, otherwise clear the block since it has nothing 
        if self.current_block_index != None:
            if self.block_occupancies[self.current_block_index] != None: # Check to update the occupancy
                self.ui.block_occupancy_combo_box.setCurrentIndex(self.block_occupancies[self.current_block_index])
            else:
                self.ui.block_occupancy_combo_box.setCurrentIndex(-1) # Set to the default no option selected

            if self.suggested_speeds[self.current_block_index] != None: 
                self.ui.suggested_speed_line_edit.setText(self.suggested_speeds[self.current_block_index])
            else:
                self.ui.suggested_speed_line_edit.clear()

            if self.suggested_authorities[self.current_block_index] != None: 
               self.ui.suggested_authority_line_edit.setText(self.suggested_authorities[self.current_block_index])
            else:
                self.ui.suggested_authority_line_edit.clear()

    @pyqtSlot()
    def handle_occupancy_confirmation(self):
        """
        Called when the confirmation next to the occupancy is clicked, writes values directly to corresponding backend controller
        """
        if self.current_block_index != None:
            if self.ui.block_occupancy_combo_box.currentIndex() == 0:
                self.collection.controllers[self.controller_index].block_occupancies[self.current_block_index] = False
                
            elif self.ui.block_occupancy_combo_box.currentIndex() == 1 or self.ui.block_occupancy_combo_box.currentIndex() == 2:
                self.collection.controllers[self.controller_index].block_occupancies[self.current_block_index] = True
    
            self.block_occupancies[self.current_block_index] = self.ui.block_occupancy_combo_box.currentIndex()
    


    @pyqtSlot()
    def handle_speed_confirmation(self):
        """
        Called when the confirmation next to the suggested speed is clicked, writes values directly to corresponding backend controller
        """
        if self.current_block_index != None:
            self.suggested_speeds[self.current_block_index] = self.ui.suggested_speed_line_edit.text()
            self.collection.controllers[self.controller_index].suggested_speeds[self.current_block_index] = float(self.ui.suggested_speed_line_edit.text())

    @pyqtSlot()
    def handle_authority_confirmation(self):
        """
        Called when the confirmation next to the suggested authority is clicked, writes values directly to corresponding backend controller
        """
        if self.current_block_index != None:
            self.suggested_authorities[self.current_block_index] = self.ui.suggested_authority_line_edit.text()
            self.collection.controllers[self.controller_index].suggested_authorities[self.current_block_index] = float(self.ui.suggested_authority_line_edit.text())
    
    @pyqtSlot()
    def handle_switch_confirmation(self):
        """
        Called when the confirmation next to the switch is clicked, writes values directly to corresponding backend controller
        """
        block = self.collection.blocks[self.current_block_index + self.block_range[0]] # lookup if the block has a switch
        if block.switch:
            self.switch_positions[self.current_block_index] = self.ui.switch_position_combo_box.currentIndex()
            self.collection.controllers[self.controller_index].switch_positions[self.current_block_index] = self.ui.switch_position_combo_box.currentIndex()

    
    @pyqtSlot()
    def handle_light_confirmation(self):
        """
        Called when the confirmation next to the switch is clicked, writes values directly to corresponding backend controller
        """
        block = self.collection.blocks[self.current_block_index + self.block_range[0]] # lookup if the block has a light
        if block.light:
            self.light_signals[self.current_block_index] = self.ui.light_signal_combo_box.currentIndex()
            self.collection.controllers[self.controller_index].light_signals[self.current_block_index] = self.ui.light_signal_combo_box.currentIndex()

    @pyqtSlot()
    def handle_crossing_confirmation(self):
        """
        Called when the confirmation next to the switch is clicked, writes values directly to corresponding backend controller
        """
        block = self.collection.blocks[self.current_block_index + self.block_range[0]] # lookup if the block has a crossing
        if block.crossing:
            self.crossing_signals[self.current_block_index] = self.ui.crossing_signal_combo_box.currentIndex()
            self.collection.controllers[self.controller_index].crossing_signals[self.current_block_index] = self.ui.crossing_signal_combo_box.currentIndex()

    def open_window(self, window_name: str):
        """
        opens the testbench window when the user switches to maintenance mode

        :param window_name: The title of the menu? window
        """
        self.collection.controllers[self.controller_index].maintenance_mode = True
        if self.first_open: # On the first time opening the testbench the ui elements need to be initialized 
            self.setWindowTitle("Wayside Testbench Module")
            self.ui.menu_Blue_Line_Controller_1.setTitle(window_name)
            self.populate_list()
            self.first_open = False

        self.show()
    
    def hide_window(self): 
        """
        My defined function for hiding the testbench window resets it to the initial condition
        """
        active_controller = self.collection.controllers[self.controller_index] # get the active train so that values can be reset
        
        # Reset the testbench values
        self.current_block_index =    None
        self.block_occupancies =     [None] * len(self.block_occupancies)
        self.suggested_speeds =      [None] * len(self.suggested_speeds)
        self.suggested_authorities = [None] * len(self.suggested_authorities)

        
        # Reset the values set to the wayside
        active_controller.block_occupancies =     [False] * len(active_controller.block_occupancies)
        active_controller.suggested_speeds =      [0] * len(active_controller.suggested_speeds)
        active_controller.suggested_authorities = [0] * len(active_controller.suggested_authorities)

        # Reset UI elements
        self.ui.block_occupancy_combo_box.setCurrentIndex(-1)
        self.ui.suggested_authority_line_edit.clear()
        self.ui.suggested_speed_line_edit.clear()
        self.ui.select_block_list.setCurrentRow(-1)
        
        self.collection.controllers[self.controller_index].maintenance_mode = False # User has closed the window so maintenance mode should no longer be active
        self.hide() # the illusion that the window is no longer with us, but really the testbench was the friends we made along the way
    
    def closeEvent(self, event):
        """
        Overridden Mainwindow function so that as long as the main wayside module is running the testbench is never fully destroyed
        """
        self.hide_window() # call the clean up to hide the window
        event.ignore() # do not let the user actually destroy the window

    def populate_list(self):
        """
        Adds entries to the list on the testbench ui corresponding to the territory the wayside controller testbench is connected to
        """
        for i in range(*self.block_range): # unpacking operator, remember ranges are [lower, upper)
            block = self.collection.blocks[i]
            text = "Block " + block.id
            if block.switch:
                text = text + ', Has Switch'
            if block.light:
                text = text + ', Has Light'
            if block.crossing:
                text = text + ', Has Crossing'
            item = QListWidgetItem(text)
            self.ui.select_block_list.addItem(item)