import matplotlib
matplotlib.use('Qt5Agg')
from time import sleep
from PyQt5 import QtTest

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.draw()
        self.axis = self.figure.add_subplot(111, position=[0.15, 0.15, 1, 1])
        self.axis.set_xlabel('Time (s)')
        self.axis.set_ylabel('Track Position (cm)')
        self.axis.xaxis.label.set_color('white')
        self.axis.yaxis.label.set_color('white')
        self.figure.patch.set_facecolor('#19232D')
        self.axis.set_facecolor('#19232D')
        self.axis.spines['bottom'].set_color('white')
        self.axis.spines['top'].set_color('white') 
        self.axis.spines['right'].set_color('white')
        self.axis.spines['left'].set_color('white')
        self.axis.tick_params(axis='both', colors='white')
        self.layoutVertical = QtWidgets.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.canvas)

class Plotter(QObject):
    finished = pyqtSignal()
    t = pyqtSignal(float)

    def run(self):
        for i in range(1000):
            QtTest.QTest.qWait(100)
            self.t.emit(i*0.1)
        self.finished.emit()

