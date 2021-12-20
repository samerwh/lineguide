from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, QSize, QThread, Qt
from qtwidgets import Toggle, AnimatedToggle
from time import sleep
import sys
import qdarkstyle
import qtwidgets
from network import *
from plot import *

class Ui_MainWindow(QtWidgets.QMainWindow):

    def setupUi(self, MainWindow):
        
        # Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        font = QtGui.QFont()

        # Plot
        self.matplotlibWidget = MatplotlibWidget(self.centralwidget)
        self.matplotlibWidget.setGeometry(QtCore.QRect(20, 0, 900, 550))
        
        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # Slider
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(100, 650, 600, 40))
        self.slider.setMaximum(37)
        self.slider.setProperty("value", 0)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("horizontal_slider")
        self.slider.valueChanged.connect(lambda: self.value_send())

        # Slider Value
        self.slider_value = QtWidgets.QLabel(self.centralwidget)
        self.slider_value.setGeometry(QtCore.QRect(750, 650, 120, 40))
        font.setPointSize(20)
        self.slider_value.setFont(font)
        self.slider_value.setObjectName("value")
        
        # Received Value
        self.received_data = QtWidgets.QLabel(self.centralwidget)
        self.received_data.setGeometry(QtCore.QRect(100, 550, 200, 30))
        font.setPointSize(12)
        self.received_data.setFont(font)
        self.received_data.setObjectName("received_data")
        
        # Options Position
        self.xpos_opts = 950
        self.ypos_opts = 70

        # IP Address Label
        self.ip_label = QtWidgets.QLabel(self.centralwidget)
        self.ip_label.setGeometry(QtCore.QRect(self.xpos_opts, self.ypos_opts, 321, 30))
        font.setPointSize(10)
        self.ip_label.setFont(font)
        self.ip_label.setObjectName("ip_label")
        
        # IP Address Input Text
        self.ipText = QtWidgets.QLineEdit(self.centralwidget)
        self.ipText.setGeometry(QtCore.QRect(self.xpos_opts, self.ypos_opts + 30, 150, 30))

        # Port Label
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setGeometry(QtCore.QRect(self.xpos_opts, self.ypos_opts + 70, 321, 30))
        font.setPointSize(10)
        self.port_label.setFont(font)
        self.port_label.setObjectName("ip_label")

        # Port Input Text
        self.portText = QtWidgets.QLineEdit(self.centralwidget)
        self.portText.setGeometry(QtCore.QRect(self.xpos_opts, self.ypos_opts + 100, 100, 30))

        # Connect Toggle
        self.toggle_1 = Toggle(self.centralwidget)
        self.toggle_1.setGeometry(QtCore.QRect(self.xpos_opts, self.ypos_opts + 150, 65, 40))
        self.toggle_1.clicked.connect(self.toggle)

        # Connect Label
        self.conn_label = QtWidgets.QLabel(self.centralwidget)
        self.conn_label.setGeometry(QtCore.QRect(self.xpos_opts + 70, self.ypos_opts + 150, 110, 40))
        font.setPointSize(10)
        self.conn_label.setFont(font)
        self.conn_label.setObjectName("conn_label")

        # Run Plot Button
        self.runplot_btn = QtWidgets.QPushButton(self.centralwidget)
        self.runplot_btn.setGeometry(QtCore.QRect(self.xpos_opts, 400, 120, 40))
        self.runplot_btn.setFont(font)
        self.runplot_btn.pressed.connect(self.run_plotter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.slider.setEnabled(False)
        self.x = [0]
        self.y = [0]
        self.last_y = 0

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "lineguide"))
        self.runplot_btn.setText(_translate("Main Window", "Run"))
        self.ip_label.setText(_translate("MainWindow", "IP Address"))
        self.port_label.setText(_translate("MainWindow", "Port"))
        self.slider_value.setText(_translate("MainWindow", "0 cm"))
        self.received_data.setText(_translate("Main Window", "Track Position: cm"))
        self.ip_label.adjustSize()
        self.port_label.adjustSize()
        self.conn_label.setText(_translate("Main Window", "Disconnected"))
    
    def toggle(self):
        if self.toggle_1.isChecked():
            self.conn_label.setText("Connecting...")
            self.connect_comms()
        else:
            self.disconnect()
            self.conn_label.setText("Disconnected")

    def value_send(self):
        i = self.slider.value()
        self.sender.value_send(i)
        self.slider_value.setText(str(i) + " cm")
        
    def report_data(self, n):
        nstr = "{:.2f}".format(n)
        self.last_y = n
        self.received_data.setText(f"Track Position: {nstr} cm")
        self.received_data.adjustSize()
    
    def report_time(self, n):
        self.x.append(n)
        self.y.append(self.last_y)
        self.matplotlibWidget.axis.clear()
        self.matplotlibWidget.axis.set_xlabel('Time (s)')
        self.matplotlibWidget.axis.set_ylabel('Track Position (cm)')
        self.matplotlibWidget.axis.plot(self.x, self.y, '#2FC5D3')
        self.matplotlibWidget.canvas.draw()

    def connect_comms(self):
        try:
            self.run_sender()
            self.run_receiver()
            self.slider.setEnabled(True)
        except:
            print("Invalid IP Address and Port")

    def run_sender(self):
        self.sender_thread = QThread()
        self.sender = Sender()
        self.sender.moveToThread(self.sender_thread)
        self.sender_thread.started.connect(self.sender.run)
        self.sender.finished2.connect(self.sender_thread.quit)
        self.sender.finished2.connect(self.sender.deleteLater)
        self.sender_thread.finished.connect(self.sender_thread.deleteLater)
        self.sender.set_ip_port(self.ipText.text(), int(self.portText.text()))
        self.sender_thread.start()

    def run_receiver(self):
        self.receiver_thread = QThread()
        self.receiver = Receiver()
        self.receiver.moveToThread(self.receiver_thread)
        self.receiver_thread.started.connect(self.receiver.run)
        self.receiver.finished.connect(self.receiver_thread.quit)
        self.receiver.finished.connect(self.receiver.deleteLater)
        self.receiver.finished.connect(self.receiver_thread.deleteLater)
        self.receiver.connected.connect(lambda: self.conn_label.setText("Connected"))
        self.receiver.progress.connect(self.report_data)
        self.receiver.set_ip_port(self.ipText.text(), int(self.portText.text()))
        self.receiver_thread.start()

    def run_plotter(self):
        self.plotter_thread = QThread()
        self.plotter = Plotter()
        self.plotter.moveToThread(self.plotter_thread)
        self.plotter_thread.started.connect(self.plotter.run)
        self.plotter.finished.connect(self.plotter_thread.quit)
        self.plotter.finished.connect(self.plotter.deleteLater)
        self.plotter_thread.finished.connect(self.plotter_thread.deleteLater)
        self.plotter.t.connect(self.report_time)
        self.plotter_thread.start()

        self.runplot_btn.setEnabled(False)
        self.plotter_thread.finished.connect(
            lambda: self.runplot_btn.setEnabled(True)
        )
    
    def disconnect(self):
        try:
            self.sender.value_send(0.01)
            self.sender.disconnect_sender()
            self.receiver.disconnect_receiver()
        except:
            pass
        self.slider.setProperty("value", 0)
        self.slider.setEnabled(False)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


