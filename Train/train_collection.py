# import sys
# sys.path.append("./Train/TrainModel")
# from train_model import TrainModel

# train_collection.py
class TrainModel:
    def __init__(self):
        # self.power = 5
        # Default UI state as strings (or numbers) that correspond to the wayside fields.
        self.ui_state = {
            "commanded_speed": "0",
            "authority": "0",
            "commanded_power": "0",
            "speed_limit": "0",
            "beacon_data": ""
        }

class TrainCollection:
    def __init__(self):
        self.train_list = []
    
    def createTrain(self):
        self.train_list.append(TrainModel())

