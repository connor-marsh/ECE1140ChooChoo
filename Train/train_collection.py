# train_collection.py
# import sys
# sys.path.append("./Train/TrainModel")
# from train_model_backend import TrainModel
# from train_model_frontend import TrainModelFrontEnd

# # train_collection.py

# class TrainCollection:
#     def __init__(self, num_trains=3):
#         self.train_list = []
#         self.train_model_ui = TrainModelFrontEnd()
#         for _ in range(num_trains):
#             self.createTrain()
#         if self.train_list:
#             self.current_train = self.train_list[0]  # Set the first train as the default.

#     def createTrain(self):
#         # Create a new TrainModel and append it to the list.
#         self.train_list.append(TrainModel())

import sys
import os
sys.path.append("./Train/TrainModel")
sys.path.append("./Train/TrainController")
from train_model_backend import TrainModel
from train_controller_backend import TrainController
from train_model_testbench import TestBenchApp as TrainModelTestbench
from PyQt5.QtWidgets import QApplication#, QMainWindow, QWidget
from PyQt5.QtCore import qInstallMessageHandler

def customMessageHandler(msg_type, context, message):
    # Filter out warnings about unknown properties.
    if "Unknown property" in message:
        return
    sys.stderr.write(message + "\n")

qInstallMessageHandler(customMessageHandler)

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class TrainCollection:
    def __init__(self, num_trains=0, model=None, controller=None):
        self.train_list = []

        # If model or controller != None, then we are running a single module with a testbench
        if model:
            self.train_model_ui = model
            self.train_controller_ui = None
        elif controller:
            self.train_controller_ui = controller
            self.train_model_ui = None
            self.train_list = []
            for _ in range(num_trains):
                self.train_list.append(TrainController())
            self.train_controller_ui.update_train_dropdown()
        else:
            # Lazy import to avoid circular dependency:
            from train_model_frontend import TrainModelFrontEnd
            self.train_model_ui = TrainModelFrontEnd(self)  # Pass self to front-end
            from train_controller_frontend import TrainControllerFrontend
            self.train_controller_ui = TrainControllerFrontend(self)
            self.train_model_ui.show()
            self.train_controller_ui.show()

        if not controller:
            self.train_list = []
            for _ in range(num_trains):
                self.createTrain()

    def createTrain(self):
        # Create a new TrainModel and append it to the list.
        self.train_list.append(TrainModel())
        if self.train_model_ui:
            self.train_model_ui.update_train_dropdown()
        if self.train_controller_ui:
            self.train_controller_ui.update_train_dropdown()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    train_collection = TrainCollection(num_trains=3)

    train_model_testbench = TrainModelTestbench(train_collection, train_integrated=True)    
    train_model_testbench.show()
    sys.exit(app.exec_())