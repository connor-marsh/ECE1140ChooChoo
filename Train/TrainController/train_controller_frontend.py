"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""
import sys
import os

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from train_controller_ui import Ui_MainWindow as TrainControllerUI

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class TrainControllerFrontend(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = TrainControllerUI()
        self.ui.setupUi(self)

    def update(self):
        pass

def main():
    app = QApplication(sys.argv)
    train_controller_frontend = TrainControllerFrontend()
    train_controller_frontend.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()