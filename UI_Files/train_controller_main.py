"""
Author: Aragya Goyal
Date: 02-16-2025
Description: 
"""
import sys
import os
import time
import math

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from train_controller_ui import Ui_MainWindow as TrainControllerUI
from train_controller_testbench_ui import Ui_TestBenchWindow as TrainControllerTestbenchUI

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

"""
Train Controller App
"""
class TrainControllerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = TrainControllerUI()
        self.ui.setupUi(self)

        self.testbench = TrainControllerTestbenchWindow(self)

"""
Train Controller Testbench
"""
class TrainControllerTestbenchWindow(QMainWindow):
    def __init__(self, train_controller_window):
        super().__init__()
        self.ui = TrainControllerTestbenchUI()
        self.ui.setupUi(self)
        self.train_controller_window = train_controller_window
    
    def read_inputs(self):
        print("hello world")
        pass

"""
Main
"""
def main():
    app = QApplication(sys.argv)
    train_controller_window = TrainControllerWindow()
    train_controller_window.show()
    train_controller_window.testbench.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()