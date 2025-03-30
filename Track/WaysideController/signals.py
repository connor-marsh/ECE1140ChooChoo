'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal



ctc_switch_states = pyqtSignal(list[bool])
ctc_exit_blocks = pyqtSignal(list[bool],list[bool],list[bool])
ctc_dispatch = pyqtSignal()
ctc_maintenance = pyqtSignal(int, bool)
ctc_suggested = pyqtSignal(list[float],list[float])


wayside_block_occupancies = pyqtSignal(list[bool])
wayside_switches = pyqtSignal(list[bool])
wayside_lights = pyqtSignal(list[bool])
wayside_crossings = pyqtSignal(list[bool])

track_tickets = pyqtSignal(int)
