'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals necessary for the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal



# A dictionary Containing the number of wayside controllers per line
CONTROLLER_COUNT = {
    "RED"   : 3,
    "GREEN" : 3,
    "BLUE"  : 1
}