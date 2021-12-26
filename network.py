from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import sleep
import socket
import pickle
import struct

class Sender(QObject):
  
    finished2 = pyqtSignal()

    def set_ip_port(self, ip, port):
        self.ip = ip
        self.port = port

    def run(self):
        print("send thread started")
        IP = self.ip 
        PORT = self.port
        self.send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.send_socket.bind((IP, PORT)) 
        self.send_socket.listen(4)
        (self.conn, (ip,port)) = self.send_socket.accept()

    def value_send(self, i):
        y = struct.pack('>d', i)
        self.conn.send(y)
        print(f"sent: {y}")

    def disconnect_sender(self):
        self.send_socket.close()
        self.finished2.emit()

class Receiver(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(float)
    connected = pyqtSignal(int)

    def set_ip_port(self, ip, port):
        self.ip = ip
        self.port = port + 1

    def run(self):
        print("rec thread started")
        IP = self.ip
        PORT = self.port
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        self.receive_socket.bind((IP, PORT))
        self.receive_socket.listen(4)

        (self.conn2, (ip,portt)) = self.receive_socket.accept()
        self.connected.emit(1)
        
        while True:
            print("rec loop")
            data = self.conn2.recv(8)
            data_str = struct.unpack('>d', data)
            print(data_str[0])
            self.progress.emit(data_str[0])

    def disconnect_receiver(self):
        self.receive_socket.close()
        self.finished.emit()



