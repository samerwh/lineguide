from PyQt5 import QtCore, QtGui, QtWidgets
from time import sleep
import sys
import qdarkstyle
import struct
from network import *

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        
        # Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu Bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        # File
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menubar.addAction(self.menufile.menuAction())

        # Status Bar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Slider
        self.slider = QtWidgets.QSlider(self.centralwidget)
        self.slider.setGeometry(QtCore.QRect(200, 400, 321, 41))
        self.slider.setMaximum(37)
        self.slider.setProperty("value", 0)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setObjectName("horizontal_slider")

        # Slider Value
        self.value = QtWidgets.QLabel(self.centralwidget)
        self.value.setGeometry(QtCore.QRect(240, 430, 321, 121))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.value.setFont(font)
        self.value.setObjectName("value")
        self.slider.valueChanged.connect(lambda: self.value_send())

        # Received Value
        self.received_data = QtWidgets.QLabel(self.centralwidget)
        self.received_data.setGeometry(QtCore.QRect(400, 300, 150, 80))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.received_data.setFont(font)
        self.received_data.setObjectName("received_data")
      
        # Label
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(240, 50, 321, 121))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label.setFont(font)
        self.label.setObjectName("label")

        # Connect Sender Button
        self.sender_btn = QtWidgets.QPushButton(self.centralwidget)
        self.sender_btn.setGeometry(QtCore.QRect(50, 200, 200, 40))
        font.setPointSize(12)
        self.sender_btn.setFont(font)
        self.sender_btn.setObjectName("sender_btn")
        self.sender_btn.pressed.connect(self.run_sender)

        # Connect Receiver Button
        self.receiver_btn = QtWidgets.QPushButton(self.centralwidget)
        self.receiver_btn.setGeometry(QtCore.QRect(50, 270, 200, 40))
        self.receiver_btn.setFont(font)
        self.receiver_btn.clicked.connect(self.run_receiver)

        # Connect Receiver Button
        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(300, 270, 200, 40))
        self.btn.setFont(font)
        self.btn.clicked.connect(lambda: self.send_btn(8))

        # MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.sender_btn.setText(_translate("MainWindow", "Connect Sender"))
        self.receiver_btn.setText(_translate("Main Window", "Connect Receiver"))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.value.setText(_translate("MainWindow", "0"))
        self.received_data.setText(_translate("Main Window", "Simulink:"))
        self.btn.setText(_translate("Main Window", "btn"))


    def value_send(self):
        i = self.slider.value()
        x.value_send(i)
        self.value.setText(str(i))

    def send_btn(self, a):
        x.value_send(a)
        
        
        

    def report_data(self, n):
        self.received_data.setText(f"Simulink: {n}")
        self.received_data.adjustSize()

    def run_sender(self):
        # Step 2: Create a QThread object
        self.sender_thread = QThread()
        # Step 3: Create a worker object
        global x
        x = self.sender = Sender()
        # Step 4: Move worker to the thread
        self.sender.moveToThread(self.sender_thread)
        # Step 5: Connect signals and slots
        self.sender_thread.started.connect(self.sender.run)
        self.sender.finished2.connect(self.sender_thread.quit)
        self.sender.finished2.connect(self.sender.deleteLater)
        #self.sender_thread.finished2.connect(self.sender_thread.deleteLater)
        # Step 6: Start the thread
        self.sender_thread.start()

        # Final resets
        self.sender_btn.setEnabled(False)
        #self.sender_thread.finished2.connect(
        #    lambda: self.sender_btn.setEnabled(True)
        #)

    def run_receiver(self):
        # Step 2: Create a QThread object
        self.receiver_thread = QThread()
        # Step 3: Create a worker object
        self.receiver = Receiver()
        # Step 4: Move worker to the thread
        self.receiver.moveToThread(self.receiver_thread)
        # Step 5: Connect signals and slots
        self.receiver_thread.started.connect(self.receiver.run)
        self.receiver.finished.connect(self.receiver_thread.quit)
        self.receiver.finished.connect(self.receiver.deleteLater)
        self.receiver_thread.finished.connect(self.receiver_thread.deleteLater)
        self.receiver.progress.connect(self.report_data)
        # Step 6: Start the thread
        self.receiver_thread.start()

        # Final resets
        self.receiver_btn.setEnabled(False)
        self.receiver_thread.finished.connect(
            lambda: self.receiver_btn.setEnabled(True)
        )
        self.receiver_thread.finished.connect(
            lambda: self.stepLabel.setText("Long-Running Step: 0")
        )

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())