import sys
import os

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, QTime, QDateTime, QObject
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

import globals.global_clock as global_clock
import globals.track_data_class as track_data
import globals.signals as signals
from Train.train_collection import TrainCollection
from Train.TrainModel.train_model_frontend import TrainModelFrontEnd
from Train.TrainModel.train_model_testbench import TrainModelTestbench
from Train.TrainController.train_controller_frontend import TrainControllerFrontend
from Train.TrainController.train_controller_testbench import TrainControllerTestbench
from Track.WaysideController.wayside_controller_collection import WaysideControllerCollection
from CTC.centralized_traffic_controller_frontend import CtcFrontEnd
from CTC.centralized_traffic_controller_backend import CtcBackEnd


if __name__=="__main__":

    running_module = "CTC" # all, CTC, WaysideController, TrackModel, Train, Train Model, Train Controller
    
    # Create App
    app = QApplication(sys.argv)

    # Setup global objects
    global_clock.init()
    track_data.init()
    signals.init()
    
    # Instatiate Modules
    if running_module == "all":
        pass
    elif running_module == "CTC":
        ctc_backend = CtcBackEnd()
        ctc_frontentd = CtcFrontEnd(ctc_backend)
        ctc_frontentd.show()
    elif running_module == "WaysideController":
        collection = WaysideControllerCollection("GREEN")
        collection.frontend.show()
    elif running_module == "TrackModel":
        pass
    elif running_module == "Train":
        train_collection = TrainCollection(num_trains=3)
        train_model_testbench = TrainModelTestbench(train_collection, train_integrated=True)    
        train_model_testbench.show()
    elif running_module == "TrainModel":
        train_model_frontend = TrainModelFrontEnd(None)
        collection = TrainCollection(num_trains=3, model=train_model_frontend)
        train_model_frontend.train_collection = collection
        train_model_frontend.update_train_dropdown()
        train_model_frontend.current_train = collection.train_list[0]
        train_model_frontend.show()
        
        train_model_testbench = TrainModelTestbench(collection)    
        train_model_testbench.show()    
    elif running_module == "TrainController":
        train_controller_frontend = TrainControllerFrontend(None, train_integrated=False)
        collection = TrainCollection(num_trains=3, controller=train_controller_frontend)
        train_controller_frontend.collection = collection
        train_controller_frontend.update_train_dropdown()
        train_controller_frontend.current_train = collection.train_list[0]
        train_controller_frontend.show()

        train_controller_testbench = TrainControllerTestbench(collection)
        train_controller_testbench.show()
    sys.exit(app.exec_())