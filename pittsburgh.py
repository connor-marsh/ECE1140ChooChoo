import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QTime, QDateTime, QObject

# from global_clock import clock
import global_clock

sys.path.append("./Train")
from train_collection import TrainCollection



if __name__=="__main__":
    app = QApplication(sys.argv)
    global_clock.init()
    
    
    train_collection = TrainCollection(num_trains=3)
    sys.exit(app.exec_())