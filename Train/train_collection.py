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
    def __init__(self):
        self.train_list = []

    def createTrain(self):
        self.train_list.append(TrainModel())
