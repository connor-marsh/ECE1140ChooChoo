"""Connor Murray breh"""
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSignal
from wayside_controller_testbench_ui import Ui_MainWindow

"""Describe the class"""
class WaysideTestbenchApp(QMainWindow):
    block_selected = pyqtSignal(str) # 
    
    def __init__(self):
        # Initialize ui from the generated designer ui
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connecting the list signals to the slot
        self.ui.select_block_list.itemClicked.connect(self.handle_block_selection)

    def handle_block_selection(self, block):
        selected_block = block.text()
        print(f"Block Selected: {selected_block}")  # Printing for testing
        self.block_selected.emit(selected_block)  # Emit signal to backend
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = WaysideTestbenchApp()
    main_window.show()
    sys.exit(app.exec_())