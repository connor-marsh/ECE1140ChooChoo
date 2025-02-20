"""
Author: Connor Murray
Date: 2/16/2025
Description: Connects the wayside controller to the testbench or other modules
             Defines wayside controller object
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject, QTimer
from wayside_controller import WaysideControllerWindow
from wayside_controller_testbench import WaysideTestbenchWindow
import sys
import wayside_constants


class controller(QObject):

    update_signal = pyqtSignal(dict)

    block_occupancies = [None] * wayside_constants.NUMBER_OF_BLOCKS # List containing the block occupancies
    suggested_speeds = [None] * wayside_constants.NUMBER_OF_BLOCKS # List contianing the suggested speeds
    suggested_authorities = [None] * wayside_constants.NUMBER_OF_BLOCKS # List containing the suggested authorities
    commanded_speeds = [None] * wayside_constants.NUMBER_OF_BLOCKS # List containing the commanded speeds
    commanded_authorities = [None] * wayside_constants.NUMBER_OF_BLOCKS # List containing the commanded speeds

    # Compiling all the lists into a dictionary so that it can be easily referenced when writing to the table
    block_table_data = {
        "Occupancy" : block_occupancies,
        "Suggested Speed" : suggested_speeds,
        "Suggested Authority" : suggested_authorities,
        "Commanded Speed" : commanded_speeds,
        "Commanded Authority" : commanded_authorities
    }

    def __init__(self):
        super().__init__()

        
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.start()
        self.timer.timeout.connect(self.send_update)
        
    
    @pyqtSlot(str, int, int, str)
    def from_testbench(self, column_header, col_index, row_index, text_value):
         self.block_table_data[column_header][row_index] = text_value
        
    @pyqtSlot()
    def send_update(self):
        self.update_signal.emit(self.block_table_data)
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wayside_window = WaysideControllerWindow()
    testbench_window = WaysideTestbenchWindow()

    w_controller = controller()

    wayside_window.show()
    testbench_window.show()

    #testbench_window.send_update_signal.connect(wayside_window.update_table_entry)
    testbench_window.send_update_signal.connect(w_controller.from_testbench)
    w_controller.update_signal.connect(wayside_window.receive_update)
    sys.exit(app.exec_())