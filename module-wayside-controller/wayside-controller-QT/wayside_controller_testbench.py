"""
Author: Connor Murray
Date: 2/16/2025
Description: 
    The class implemented here builds on the generated QT desinger output for the wayside controller testbench ui.
"""
import sys
import wayside_constants
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIntValidator
from wayside_controller_testbench_ui import Ui_MainWindow


class WaysideTestbenchWindow(QMainWindow):
    """
    Describe the class
    """

    
    
    # Variables
    current_block_index = None # index to the lists below
    block_occupancies = ["Unoccupied"] * wayside_constants.NUMBER_OF_BLOCKS # List containing the block occupancies
    suggested_authorities = [None] * wayside_constants.NUMBER_OF_BLOCKS # List containing the suggested authorities
    suggested_speeds = [None] * wayside_constants.NUMBER_OF_BLOCKS # List contianing the suggested speeds


    # Signals specifying which block and the value to update with
    send_update_signal = pyqtSignal(str, int, str) # (row, index, value)
    

    def __init__(self):
        """
        initializes the frontend logic of the testbench
        """
        
        super().__init__() # Initialize ui from the generated designer ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_validators()

       
        self.ui.select_block_list.itemClicked.connect(self.handle_block_selection)  # Connecting the list signals to the slot
        self.ui.suggested_speed_confirm_button.clicked.connect(self.handle_speed_confirmation)
        self.ui.suggested_authority_confirm_button.clicked.connect(self.handle_authority_confirmation)
        self.ui.block_occupancy_confirm_button.clicked.connect(self.handle_occupancy_confirmation)


    def setup_validators(self):
        """
        Specifies that the line edits on the page can only have integer values
        """
        speed_validator = QIntValidator(0, 10000) # convert to mph since entry is done in mph
        self.ui.suggested_speed_line_edit.setValidator(speed_validator)

        authority_validator = QIntValidator(0, 10000)
        self.ui.suggested_authority_line_edit.setValidator(authority_validator)


    @pyqtSlot(QListWidgetItem)  
    def handle_block_selection(self, selected_block):
        """
        Updates the UI after a block has been selected from the list
        :params selected_block: The QListItem chosen 
        """
        self.current_block_index = self.ui.select_block_list.row(selected_block) # Updating the index based on the block selected
        
        # Update the gui so that it reflects what the user has input previously, or if yet to input anything set to defaults
        # Update combo box for block occupancy 
        if(self.block_occupancies[self.current_block_index] == "Unoccupied"):
            self.ui.block_occupancy_combo_box.setCurrentIndex(0) # match combo box to unoccupied if never accessed before or has been set to Unoccupied
        elif(self.block_occupancies[self.current_block_index] == "Occupied"):
            self.ui.block_occupancy_combo_box.setCurrentIndex(1) # match combo box to the user input of occupied
        elif(self.block_occupancies[self.current_block_index] == "Maintenance"):
            self.ui.block_occupancy_combo_box.setCurrentIndex(2) # match combo box to the user input of maintenance
        elif(self.block_occupancies[self.current_block_index] == "Track Failure"):
            self.ui.block_occupancy_combo_box.setCurrentIndex(3) # match combo box to the user input of track failure

        # Update the suggested speed fields to match the corresponding blocks user input, otherwise clear the block since it has nothing 
        if self.suggested_speeds[self.current_block_index] == None:
            self.ui.suggested_speed_line_edit.clear()
            self.ui.suggested_authority_line_edit.clear()
        else:
            self.ui.suggested_speed_line_edit.setText(self.suggested_speeds[self.current_block_index])
            self.ui.suggested_authority_line_edit.setText(self.suggested_authorities[self.current_block_index])

        # Update the suggested authority fields to match the corresponding blocks user input, otherwise clear the block since it has nothing 
        if self.suggested_authorities[self.current_block_index] == None:
            self.ui.suggested_authority_line_edit.clear()
        else:
            self.ui.suggested_authority_line_edit.setText(self.suggested_authorities[self.current_block_index])
    
    
    @pyqtSlot()
    def handle_speed_confirmation(self):
        """
        define function
        params:
        """
        if self.current_block_index is not None: # Making sure the confirmation button only updates when a block is selected
            # When the confirm button is clicked update the speed and emit a signal
            self.suggested_speeds[self.current_block_index] = self.ui.suggested_speed_line_edit.text()
            self.send_update_signal.emit("Suggested Speed",self.current_block_index, self.ui.suggested_speed_line_edit.text())
    
   
    @pyqtSlot()  
    def handle_authority_confirmation(self):
        """
        define function
        params:
        """
        if self.current_block_index is not None: # Making sure the confirmation button only updates when a block is selected
            # When the confirm button is clicked update the authority and emit a signal
            self.suggested_authorities[self.current_block_index] = self.ui.suggested_authority_line_edit.text()
            self.send_update_signal.emit("Suggested Authority", self.current_block_index, self.ui.suggested_authority_line_edit.text())
    
    
    @pyqtSlot()
    def handle_occupancy_confirmation(self):
        """
        define function
        params:
        """
        if self.current_block_index is not None: # Making sure the confirmation button only updates when a block is selected
            # When the confirm button is clicked update the occupancy in accordance with the current state of the combo box
            self.block_occupancies[self.current_block_index] = self.ui.block_occupancy_combo_box.currentText()
            self.send_update_signal.emit("Occupancy", self.current_block_index, self.ui.block_occupancy_combo_box.currentText())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WaysideTestbenchWindow()
    main_window.show()
    sys.exit(app.exec_())