"""
Author: Connor Murray
Date: 2/16/2025
Description: 
    The class implemented here builds on the generated QT desinger output for the wayside controller testbench ui.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from wayside_controller_ui import Ui_MainWindow

class WaysideControllerApp(QMainWindow):
    """
    Describe the class
    """

    def __init__(self):
        """
        Describe the function
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_table(self.ui.junction_table.horizontalHeader(), self.ui.junction_table.verticalHeader())

    def setup_table(self, col_header, row_header):
        """
        Resizes the table to fit the desired space
        """

        # Make all columns stretch equally
        for col in range(self.ui.junction_table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)

        for row in range(self.ui.junction_table.rowCount()):
            row_header.setSectionResizeMode(row, QHeaderView.Stretch)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = WaysideControllerApp()
    main_window.show()
    sys.exit(app.exec_())