from enum import Enum
"""
Enum Types File
"""
class Occupancy(Enum):
    UNOCCUPIED = 0
    OCCUPIED = 1
    MAINTENANCE = 2
    FAILURE = 3

class Failures(Enum):
    NONE = 0
    TRACK_CIRCUIT_FAILURE = 1
    POWER_FAILURE = 2
    BROKEN_RAIL_FAILURE = 3

class BoardingSide(Enum):
    LEFT = 0
    RIGHT = 1
    LEFTANDRIGHT = 2
