import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from train_controller_ui import Ui_MainWindow
from train_controller_ui_b import Ui_Form

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Set up UI from Qt Designer
        self.second_window = None  # Placeholder for second window

        # Connect button to open second window
        self.test_bench_button.clicked.connect(self.open_second_window)

    def open_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow()
        self.second_window.show()

class SecondWindow(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Set up UI from Qt Designer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
