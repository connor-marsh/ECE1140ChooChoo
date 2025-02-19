"""
Author: Connor Murray
Date: 2/16/2025
Description: The class implemented here builds on the generated QT desinger output for the wayside controller testbench ui.
"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidget, QTableWidgetItem
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from wayside_controller_ui import Ui_MainWindow

class WaysideControllerWindow(QMainWindow):
    """
    Initializes the window for the wayside controller and implements the logic for displaying the necessary information to the user
    """
    editable_columns_block_table = [3,4]
    editable_columns_junction_table = [1,2]
    gui_table_data = pyqtSignal(dict, dict) # first dictionary corresponds to block table, second corresponds to junction table

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
        self.set_column_editable(self.ui.junction_table, self.editable_columns_junction_table)
        self.set_column_editable(self.ui.block_table, self.editable_columns_block_table)
        
        
        # Connecting signals from the ui elements
        self.ui.mode_select_combo_box.activated.connect(self.handle_mode_switch)


    def setup_table_dimensions(self, table):
        """
        Used in table initialization, resizes the table to fit the desired space
        
        :param table: A QTableWidget
        """

        col_header = table.horizontalHeader()

        # Make all columns stretch equally
        for col in range(table.columnCount()):
            col_header.setSectionResizeMode(col, QHeaderView.Stretch)

        
        

    def set_column_editable(self, table, columns):
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
                    if col in columns: # Check to see if the column should be editable
                        item.setFlags(item.flags() | Qt.ItemIsEditable)  # Make editable
                    else:
                        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make non-editable
 

    @pyqtSlot(QTableWidget, dict, list)
    def update_table_data(self, table, data_dict, columns):
        """
        Will write the information in the dictionary so that it is displayed on the ui

        :param table: A QTableWidget to be altered
        :param data_dict: A dictionary containing the information to display
                          example  (key = block, value = list[occupancy, suggested speed, suggested authority, commanded speed, commanded authority])
        :param columns: a list of columns to write to
        """
        # Update the number of rows in the table based off of the dictionary
        table.setRowCount(len(data_dict))

        # Loop through each item in the table
        row = 0
        for key in data_dict:
            col = 0
            for value in data_dict[key]:
                if col in columns:
                    item = QTableWidgetItem(str(value))
                    table.setItem(row, col, item)
                col += 1
            row += 1

    def extract_table_data(self, table, columns):
        """
        Takes data from the QTableWidget and puts it into a dictionary that can be interpreted by the backend
        
        :param table: A QTableWidget
        :param columns: A list of columns to extract from
        :return data_dict: A dictionary containing the entries of the table
        """
        data_dict = {}
        for row in range(table.rowCount()):
            row_data = []
            for col in columns:
                item = table.item(row, columns)
                # Get text if item exists, otherwise empty string
                row_data.append(item.text() if item is not None else '')
            data_dict[row + 1] = row_data # want the rows to match the gui so index from 1
        return data_dict

    @pyqtSlot()
    def handle_input_confirmation(self):
        """
        Handler that emits a signal containing the changed data in the block table when the user clicks the confirm button
        """
        
        # Change in data confirmed, extract data from tables
        block_data = self.extract_table_data(self.ui.block_table)
        junction_data = self.extract_table_data(self.ui.junction_table)

        # Emit a signal so that the backend receives the data
        self.gui_table_data.emit(block_data, junction_data)


        
        
       
        
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
            self.ui.confirm_button.setStyleSheet("background-color: rgb(157, 157, 157);")
            self.ui.confirm_button.clicked.disconnect(self.handle_input_confirmation)
        else:
            self.ui.junction_table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.ui.block_table.setEditTriggers(QTableWidget.AllEditTriggers)
            self.ui.confirm_button.setStyleSheet("background-color: rgb(110, 255, 102);")
            self.ui.confirm_button.clicked.connect(self.handle_input_confirmation)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WaysideControllerWindow()
    main_window.show()
    sys.exit(app.exec_())