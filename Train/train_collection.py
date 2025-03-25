# import sys
# sys.path.append("./Train/TrainModel")
# from train_model import TrainModel

# train_collection.py
class TrainModel:
    def __init__(self):
        # Default UI data for wayside and auxiliary functions.
        self.ui_data = {
            "commanded_speed": 0.0,
            "authority": 0.0,
            "commanded_power": 0.0,
            "speed_limit": 0.0,
            "beacon_data": "",
            "announcements": "",
            "grade": 0.0,
            "passenger_count": 0.0,
            "crew_count": 0.0,
            "emergency_brake": False,
            # Add any other auxiliary fields (except cabin crew) as needed.
        }
        # Default simulation state (cabin temperature is not part of UI_data)
        self.sim_state = {
            "actual_velocity": 0.0,
            "current_acceleration": 0.0,
            "previous_acceleration": 0.0,
            "cabin_temp": 25.0
        }

class TrainCollection:
    def __init__(self, num_trains=3):
        self.train_list = []
        self.current_train = None  # This will store the default/current train.
        for _ in range(num_trains):
            self.createTrain()
        if self.train_list:
            self.current_train = self.train_list[0]  # Set the first train as the default.

    def createTrain(self):
        # Create a new TrainModel and append it to the list.
        self.train_list.append(TrainModel())