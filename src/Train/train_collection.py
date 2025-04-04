import sys
import os

from Train.TrainModel.train_model_backend import TrainModel
from Train.TrainModel.train_model_testbench import TrainModelTestbench
from Train.TrainController.train_controller_backend import TrainController
from globals.settings import USING_HARDWARE

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
        self.hardware_active = False

        # If model or controller != None, then we are running a single module with a testbench
        if model:
            self.train_model_ui = model
            self.train_controller_ui = None
            self.train_list = []
            for _ in range(num_trains):
                self.train_list.append(TrainModel(train_integrated=False))
        elif controller:
            self.train_controller_ui = controller
            self.train_model_ui = None
            self.train_list = []
            for _ in range(num_trains):
                self.train_list.append(TrainController(train_integrated=False))
            self.train_controller_ui.update_train_dropdown()
        else:
            # Lazy import to avoid circular dependency:
            from Train.TrainModel.train_model_frontend import TrainModelFrontEnd
            self.train_model_ui = TrainModelFrontEnd(self)  # Pass self to front-end
            from Train.TrainController.train_controller_frontend import TrainControllerFrontend
            self.train_controller_ui = TrainControllerFrontend(self)
            self.train_model_ui.show()
            self.train_controller_ui.show()
            self.train_list = []
            for _ in range(num_trains):
                self.create_train()

    def create_train(self):
        # Create a new TrainModel and append it to the list.
        if USING_HARDWARE and not self.hardware_active and len(self.train_list)>0:
            self.train_list.append(TrainModel(hardware_controller=True))
            self.hardware_active = True
        else:
            self.train_list.append(TrainModel())
        self.train_model_ui.update_train_dropdown()
        self.train_controller_ui.update_train_dropdown()
    
    def remove_train(self, idx):
        self.train_list.pop(idx)
        self.train_model_ui.update_train_dropdown()
        self.train_controller_ui.update_train_dropdown()

    # IMPORTANT NOTE
    # WHEN REMOVING TRAIN, CHECK type(train.controller) and if its HW
    # THEN SET self.hardware_active = False
    def removeTrain(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    train_collection = TrainCollection(num_trains=3)

    train_model_testbench = TrainModelTestbench(train_collection, train_integrated=True)    
    train_model_testbench.show()
    sys.exit(app.exec_())