import sys
import os
# from PySide2.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from TrainModel_UI_Iteration_1 import Ui_MainWindow

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class TrainModelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
