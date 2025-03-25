

#These are from my old cold and will probably be removed
NUMBER_OF_BLOCKS = 15 
MAX_SPEED_LIMIT = 50 # kmh 
MAX_AUTHORITY = 500 # m
NUMBER_OF_JUNCTIONS = 1
# IGNORE ABOVE

"""
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary Constant Values for the Wayside Controller
"""
# A dictionary containing the number of wayside controllers per line
CONTROLLER_COUNT = {
    "RED"   : 3,
    "GREEN" : 3
}

# A dictionary that contains the range of each controller
BLOCK_COUNT = {
    "RED"   : [3,2,1],
    "GREEN" : [3,2,1]
}

# A dictionary that contains the number of switches of each controller
SWITCH_COUNT = {
    "RED"   : [3,2,1],
    "GREEN" : [3,2,1]
}

# A dictionary of constant values that contains the number of crossings of each controller
CROSSING_COUNT = {
    "RED"   : [1,1,1],
    "GREEN" : [1,1,1]
}

# A dictionary of constant values that contains the number of lights of each controller
LIGHT_COUNT = {
    "RED"   : [1,1,1],
    "GREEN" : [1,1,1]
}

# A dictionary of constant values that contains the number of exit blocks of each controller
EXIT_BLOCK_COUNT = {
    "RED"   : [1,1,1],
    "GREEN" : [1,1,1]
}