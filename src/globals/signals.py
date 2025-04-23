'''
Author: Connor Murray
Date: 3/20/2025
Description: 
    Lists the necessary pyqt signals the Track Model, Wayside Controller, and CTC to communicate.
'''


from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    ctc_switch_maintenance = { 'Green' : pyqtSignal(str, bool),
                                'Red'  : pyqtSignal(str, bool)}
    
    ctc_exit_blocks = {'Green' : pyqtSignal(list),
                       'Red'   : pyqtSignal(list)}
    
    
    ctc_dispatch = {'Green' : pyqtSignal(),
                    'Red'   : pyqtSignal()}
    
    
    ctc_block_maintenance = {'Green' : pyqtSignal(str, bool),
                             'Red'   : pyqtSignal(str, bool)}
    
    
    ctc_suggested = {'Green' : pyqtSignal(dict, dict),
                     'Red'   : pyqtSignal(dict, dict)}


    wayside_block_occupancies = pyqtSignal(dict, str)
    wayside_plc_outputs = pyqtSignal(list,list,list,list, str)

    track_tickets = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

    
    
def init():
    global communication
    communication = Signals()
