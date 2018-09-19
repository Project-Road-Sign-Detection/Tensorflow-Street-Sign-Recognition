from PyQt5.QtGui import QColor
from time import time
import datetime


class GuiLogger:

    def __init__(self, view):
        self.view = view
        self.red = QColor(255, 0, 0)
        self.green = QColor(0, 255, 0)

    def log_err(self, msg):
        ts = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.view.error.setTextColor(self.red)
        self.view.error.append(ts+" "+msg)

    def log(self, msg):
        ts = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
        self.view.error.setTextColor(self.green)
        self.view.error.append(ts+" "+msg)

    def clear(self):
        self.view.error.setText("")