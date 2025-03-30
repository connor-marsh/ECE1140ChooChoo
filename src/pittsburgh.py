import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QTime, QDateTime, QObject

import src.global_clock as global_clock
from src.Train.train_collection import TrainCollection



if __name__=="__main__":
    os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    app = QApplication(sys.argv)
    global_clock.init()
    
    
    train_collection = TrainCollection(num_trains=3)
    sys.exit(app.exec_())