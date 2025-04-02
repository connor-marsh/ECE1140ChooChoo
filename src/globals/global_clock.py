from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, QTime

class GlobalClock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.am_pm = "AM"
        self.text = "06:59"
        self.hour = 6
        self.minute = 59
        
        # update speeds for the various modules
        self.time_multiplier = 1
        self.train_dt=1

        self.time = QTime(6, 59, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)
        
    def update(self):
        self.time = self.time.addSecs(self.time_multiplier)
        self.hour = self.time.hour()
        self.minute = self.time.minute()
        self.am_pm = "AM" if self.hour < 12 else "PM"
        self.hour = self.hour % 12 or 12
        self.text = f"{self.hour:02d}:{self.minute:02d}"

def init():
    global clock
    clock = GlobalClock()