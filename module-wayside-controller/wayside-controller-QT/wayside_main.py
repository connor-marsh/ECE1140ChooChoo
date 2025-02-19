"""
Author: Connor Murray
Date: 2/16/2025
Description: Connects the wayside controller to the testbench or other modules
             Defines wayside controller object
"""

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from wayside_controller import WaysideControllerWindow
from wayside_controller_testbench import WaysideTestbenchWindow
import sys



        

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wayside_window = WaysideControllerWindow()
    testbench_window = WaysideTestbenchWindow()

    

    wayside_window.show()
    testbench_window.show()
    sys.exit(app.exec_())