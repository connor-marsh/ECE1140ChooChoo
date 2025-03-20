import sys
sys.path.append("./Train/TrainModel")
from train_model import TrainModel

class TrainCollection():
    def __init__(self):
        self.train_list = []
    
    def createTrain(self):
        self.train_list.append(TrainModel())