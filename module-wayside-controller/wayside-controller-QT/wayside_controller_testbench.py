"""Connor Murray breh"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal
from wayside_controller_testbench_ui import Ui_MainWindow

"""Describe the class"""
class WaysideTestbenchApp(QMainWindow):
    
    # Constants
    NUMBER_OF_BLOCKS = 15 # constant value

    # Variables
    current_block_index = None # index to the lists below
    block_occupancies = ["Unoccupied"] * NUMBER_OF_BLOCKS # List containing the block occupancies
    suggested_authorities = ["Not Set"] * NUMBER_OF_BLOCKS # List containing the suggested authorities
    suggested_speeds = ["Not Set"] * NUMBER_OF_BLOCKS # List contianing the suggested speeds

    # Signals specifying which block and the value to update with
    block_occupancy = pyqtSignal(int, str) # (index, value)
    suggested_authority = pyqtSignal(int, str) # (index, value)
    suggested_speed = pyqtSignal(int, str) # (index, value)


    def __init__(self):
        # Initialize ui from the generated designer ui
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connecting the list signals to the slot
        self.ui.select_block_list.itemClicked.connect(self.handle_block_selection)
        self.ui.suggested_speed_confirm_button.clicked.connect(self.handle_speed_confirmation)
        self.ui.suggested_authority_confirm_button.clicked.connect(self.handle_authority_confirmation)
        
    def handle_block_selection(self, selected_block):
        self.current_block_index = self.ui.select_block_list.row(selected_block) + 1 # Updating the index based on the block selected (use 1 indexing)
        
        # Update the suggested speed fields to match the corresponding blocks user input, otherwise clear the block since it has nothing 
        if self.suggested_speeds[self.current_block_index] == "Not Set":
            self.ui.suggested_speed_line_edit.clear()
            self.ui.suggested_authority_line_edit.clear()
        else:
            self.ui.suggested_speed_line_edit.setText(self.suggested_speeds[self.current_block_index])
            self.ui.suggested_authority_line_edit.setText(self.suggested_authorities[self.current_block_index])

        # Update the suggested authority fields to match the corresponding blocks user input, otherwise clear the block since it has nothing 
        if self.suggested_authorities[self.current_block_index] == "Not Set":
            self.ui.suggested_authority_line_edit.clear()
        else:
            self.ui.suggested_authority_line_edit.setText(self.suggested_authorities[self.current_block_index])

    def handle_speed_confirmation(self):
        # When the confirm button is clicked update the speed and emit a signal
        self.suggested_speeds[self.current_block_index] = self.ui.suggested_speed_line_edit.text()
        self.suggested_speed.emit(self.current_block_index, self.ui.suggested_speed_line_edit.text())
         
    def handle_authority_confirmation(self):
        # When the confirm button is clicked update the authority and emit a signal
        self.suggested_authorities[self.current_block_index] = self.ui.suggested_authority_line_edit.text()
        self.suggested_authority.emit(self.current_block_index, self.ui.suggested_authority_line_edit.text())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WaysideTestbenchApp()
    main_window.show()
    sys.exit(app.exec_())