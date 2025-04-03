'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    ctc_switch_maintenance = pyqtSignal(str, bool) 
    ctc_exit_blocks = pyqtSignal(list)
    ctc_dispatch = pyqtSignal()
    ctc_block_maintenance = pyqtSignal(str, bool)
    ctc_suggested = pyqtSignal(dict,dict)


    wayside_block_occupancies = pyqtSignal(list)
    wayside_switches = pyqtSignal(list)
    wayside_lights = pyqtSignal(list)
    wayside_crossings = pyqtSignal(list)

    track_tickets = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    
    
def init():
    global communication
    communication = Signals()
