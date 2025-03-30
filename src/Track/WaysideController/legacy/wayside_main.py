"""
Author: Connor Murray
Date: 2/16/2025
Description: Connects the wayside controller to the testbench or other modules
             Defines wayside controller object
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QObject, QTimer
from src.Track.WaysideController.legacy.wayside_controller import WaysideControllerWindow
from wayside_controller_testbench import WaysideTestbenchWindow
import sys
import wayside_constants


class Controller(QObject):

    update_signal = pyqtSignal(dict, dict)
    
    manual_mode = False
    block_occupancies = ["Unoccupied"] * wayside_constants.NUMBER_OF_BLOCKS # List containing the block occupancies
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

    junction_table_data = {
        "Junction" : ["A5-B6-C11"] * wayside_constants.NUMBER_OF_JUNCTIONS,
        "Light Signals" : ["Red, Red"] * wayside_constants.NUMBER_OF_JUNCTIONS,
        "Switch Position" : ["A5 -B6"] * wayside_constants.NUMBER_OF_JUNCTIONS
    }

    def __init__(self):
        super().__init__()

        
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.start()
        self.timer.timeout.connect(self.send_update)
        
    
    @pyqtSlot(str, int, str)
    def from_testbench(self, column_header, row_index, text_value):
         self.block_table_data[column_header][row_index] = text_value
    
    @pyqtSlot(dict)
    def from_ui(self, data):
        
        valid_speed = self.validate_data("Commanded Speed",data["Commanded Speed"])
        valid_authority = self.validate_data("Commanded Authority",data["Commanded Authority"])
        self.block_table_data["Commanded Speed"] = valid_speed
        self.block_table_data["Commanded Authority"] = valid_authority
        
    @pyqtSlot()
    def send_update(self):
        for block in self.block_table_data["Occupancy"]:
            row = 0
            if block == "Occupied" and self.manual_mode == False:
                self.block_table_data["Commanded Speed"][row] = self.block_table_data["Suggested Speed"][row]
                self.block_table_data["Commanded Authority"][row] = self.block_table_data["Suggested Authority"][row]
                row += 1

        valid_speed = self.validate_data("Commanded Speed", self.block_table_data["Commanded Speed"])
        valid_authority = self.validate_data("Commanded Authority", self.block_table_data["Commanded Authority"])
        self.block_table_data["Commanded Speed"] = valid_speed
        self.block_table_data["Commanded Authority"] = valid_authority

        self.update_signal.emit(self.block_table_data, self.junction_table_data)
    
    def validate_data(self, key, data):
        valid = []
        if(key == "Commanded Speed"):
            for item in data:
                row = 0
                if item != None:
                    if item == "Occupied" and self.manual_mode == False:
                        number = min(int(item), int(wayside_constants.MAX_SPEED_LIMIT * 0.621), int(self.block_table_data["Suggested Speed"][row]))
                        valid.append(str(number))
                    else:
                        number = min(int(item), int(wayside_constants.MAX_SPEED_LIMIT * 0.621))
                        valid.append(str(number))
                else:
                    valid.append(None)
                row =+ 1
        else:
            for item in data:
                row = 0
                if item != None:
                    if item == "Occupied" and self.manual_mode == False:
                        number = min(int(item), int(wayside_constants.MAX_AUTHORITY * 3.28), int(self.block_table_data["Suggested Authority"][row]))
                        valid.append(str(number))
                    else:
                        number = min(int(item), int(wayside_constants.MAX_AUTHORITY * 3.28))
                        valid.append(str(number))
                else:
                    valid.append(None)
                row =+ 1
        return valid
    
    @pyqtSlot(bool)
    def set_manual_mode(self, current_mode):
        self.manual_mode = current_mode
        print(self.manual_mode)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wayside_window = WaysideControllerWindow()
    testbench_window = WaysideTestbenchWindow()

    w_controller = Controller()

    wayside_window.show()
    testbench_window.show()

    testbench_window.send_update_signal.connect(w_controller.from_testbench)
    w_controller.update_signal.connect(wayside_window.receive_update)
    wayside_window.gui_table_data.connect(w_controller.from_ui)
    wayside_window.manual_mode.connect(w_controller.set_manual_mode)

    sys.exit(app.exec_())