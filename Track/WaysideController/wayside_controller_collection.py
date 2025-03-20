import sys
import track_constants
import signals
from wayside_controller_front import WaysideFrontend
from wayside_controller_back import Controller


class WaysideControllerCollection():
    """
    A class that contains several wayside controllers and handles interfacing with the other modules such as the Track Model and The CTC.
    The front end that will display information about the currently selected wayside controller is also contained in this class.
    """

    def __init__(self, line_name):
        """
        the initialization function will use constants in reference to the line name
        """
        controllers = [Controller] * track_constants.CONTROLLER_COUNT[line_name]
        frontend = WaysideFrontend
