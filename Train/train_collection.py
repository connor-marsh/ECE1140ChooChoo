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
sys.path.append("./Train/TrainModel")
sys.path.append("./Train/TrainController")
from train_model_backend import TrainModel
from train_controller_backend import TrainController

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
        else:
            self.current_train = None
        # Lazy import to avoid circular dependency:
        from train_model_frontend import TrainModelFrontEnd
        self.train_model_ui = TrainModelFrontEnd(self)  # Pass self to front-end
        from train_controller_frontend import TrainControllerFrontend
        self.train_controller_ui = TrainControllerFrontend(self)

        if not controller:
            self.train_list = []
            for _ in range(num_trains):
                self.createTrain()

    def createTrain(self):
        # Create a new TrainModel and append it to the list.
        self.train_list.append(TrainModel())
