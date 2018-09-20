from PyQt5.QtGui import QColor
from time import time
import datetime
import string

class GuiLogger:

    def __init__(self, view):
        self.view = view
        self.red = QColor(255, 0, 0)
        self.black = QColor(0, 0, 0)
        self.green = QColor(0, 255, 0)

    def log_err(self, msg):
        ts = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.view.error.setTextColor(self.red)
        self.view.error.append(ts+" "+msg)

    def log(self, msg):
        ts = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.view.error.setTextColor(self.black)
        self.view.error.append(ts+" "+msg)

    def log_sep(self, msg = None):
        self.view.error.setTextColor(self.black)
        if msg:
            m = msg.center(120, '-')
            self.view.error.append(m)
        else:
            self.view.error.append(120*'-')

    def clear(self):
        self.view.error.setText("")