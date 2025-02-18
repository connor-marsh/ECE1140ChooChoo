"""
Author: Connor Murray
Date: 2/16/2025
Description: The class implemented here builds on the generated QT desinger output for the wayside controller testbench ui.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from wayside_controller_ui import Ui_MainWindow

class WaysideControllerWindow(QMainWindow):
    """
    Initializes the window for the wayside controller and implements the logic for displaying the necessary information to the user
    """
    
    mode = pyqtSignal(str)

    def __init__(self):
        """
        Initializes the wayside controller window
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setting up the tables
        self.setup_table_dimensions(self.ui.junction_table)
        self.setup_table_dimensions(self.ui.block_table)
        self.set_column_editable(self.ui.junction_table, [1,2])
        self.set_column_editable(self.ui.block_table, [3,4])

       
        
        self.ui.mode_select_combo_box.activated.connect(self.handle_mode_switch)

    def setup_table_dimensions(self, table):
        """
        Used in table initialization, resizes the table to fit the desired space
        
        :param table: A QTableWidget
        """

        col_header = table.horizontalHeader()
        row_header = table.verticalHeader()

        # Make all columns stretch equally
        for col in range(table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)

        # Make all rows stretch equally
        for row in range(table.rowCount()):
            row_header.setSectionResizeMode(row, QHeaderView.Stretch)
        
        table.resizeColumnsToContents()

    def set_column_editable(self, table, column):
        """
        Used for table initialization, set the editability of an entire column in a QT table.

        :param table: A QTableWidget
        :param column: List of column indices to make editable
        """
        # Loop through each item in the table
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                item = table.item(row, col) # Get the item
                if item:  # Check if the item exists (breaks if value == none)
                    if col in column: # Check to see if the column should be editable
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Make editable
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make non-editable

    @pyqtSlot(int)
    def handle_mode_switch(self, mode):
        """
        Handler that toggles whether the table entries can be editted or not
        """
        # mode == 0 indicates automatic, mode == 1 indicates maintenance
        if mode == 0: 
            # Make it so that no items in the table are editable
            self.ui.junction_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.ui.block_table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.mode.emit("Automatic Mode")
        else:
            self.ui.junction_table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.ui.block_table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.mode.emit("Maintenance Mode")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WaysideControllerWindow()
    main_window.show()
    sys.exit(app.exec_())