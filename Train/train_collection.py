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

class TrainCollection:
    def __init__(self, num_trains=0):
        self.train_list = []
        for _ in range(num_trains):
            self.createTrain()
        # Lazy import to avoid circular dependency:
        from train_model_frontend import TrainModelFrontEnd
        self.train_model_ui = TrainModelFrontEnd(self)  # Pass self to front-end
        from train_controller_frontend import TrainControllerFrontEnd
        self.train_controller_ui = TrainControllerFrontEnd(self)

    def createTrain(self):
        # Create a new TrainModel and append it to the list.
        self.train_list.append(TrainModel())
