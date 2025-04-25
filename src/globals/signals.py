'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal, QObject


class SignalsCtc(QObject):
    ctc_switch_maintenance = pyqtSignal(str, bool)
    
    ctc_exit_blocks = pyqtSignal(list)
    
    
    ctc_dispatch = pyqtSignal()
    
    
    ctc_block_maintenance = pyqtSignal(str, bool)
    
    
    ctc_suggested = pyqtSignal(dict, dict)

    def __init__(self):
        super().__init__()

class SignalsTrack(QObject):
    wayside_block_occupancies = pyqtSignal(dict, str) # block occupancies sent to the ctc, dictionary of occupacies then string for line name

    wayside_plc_outputs = pyqtSignal(list,list,list,list, str) # wayside plc outputs sent to the ctc, sorted list of blocks, switches, lights, crossings, and line name

    track_tickets = pyqtSignal(int, str) # track model sends the ticket count to the ctc, integer value representing count then string for line name

    track_temperature = pyqtSignal(float, str)  # temperature + line name
    def __init__(self):
        super().__init__()

    
def init():
    global communication_ctc
    global communication_track

    communication_ctc = {} # can add more ctc channels for each track similar to track data class
    communication_ctc["Green"] = SignalsCtc()

    communication_track = SignalsTrack() # ctc wants all tracks to connect back but specify which line it was from in argument
