'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal, pyqtSlot



ctc_switch_states = pyqtSignal(list)
ctc_exit_blocks = pyqtSignal(list,list,list)
ctc_dispatch = pyqtSignal()
ctc_maintenance = pyqtSignal(int, bool)
ctc_suggested = pyqtSignal(list,list)


wayside_block_occupancies = pyqtSignal(list)
wayside_switches = pyqtSignal(list)
wayside_lights = pyqtSignal(list)
wayside_crossings = pyqtSignal(list)

track_tickets = pyqtSignal(int)