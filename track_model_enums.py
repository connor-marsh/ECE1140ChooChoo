from enum import Enum
"""
Enum Types File
"""
class Occupancy(Enum):
    UNOCCUPIED = "Unoccupied"
    OCCUPIED = "Occupied"
    MAINTENANCE = "Maintenance"
    FAILURE = "Failure"

class Failures(Enum):
    NONE = "None"
    TRACK_CIRCUIT_FAILURE = "Track Circuit Failure"
    POWER_FAILURE = "Power Failure"
    BROKEN_RAIL_FAILURE = "Broken Rail Failure"

class BoardingSide(Enum):
    LEFT = "Left"
    RIGHT = "Right"
    LEFTANDRIGHT = "Left and Right"
