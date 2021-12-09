from PyQt5.QtCore import QObject, QThread, pyqtSignal
from time import sleep
import socket
import struct

class Sender(QObject):
  
    finished2 = pyqtSignal()

    def run(self):
        print("send thread started")
        TCP_IP = '192.168.137.187' 
        TCP_PORT = 9000 
        BUFFER_SIZE = 20
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        send_socket.bind((TCP_IP, TCP_PORT)) 
        send_socket.listen(4)
        global conn
        (conn, (ip,port)) = send_socket.accept()

    def value_send(self, i):
        y = struct.pack('>d', i)
        conn.send(y)
        print(f"sent: {y}")

class Receiver(QObject):

    finished = pyqtSignal()
    progress = pyqtSignal(float)

    def run(self):
        print("rec thread started")
        host = '192.168.137.187'
        port = 9001
        BUFFER_SIZE = 2000
        receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
        receive_socket.bind((host, port))
        receive_socket.listen(4)

        global conn2
        (conn2, (ip,portt)) = receive_socket.accept()
        
        while True:
            print("rec loop")
            data = conn2.recv(8)
            data_str = struct.unpack('>d', data)
            print(data_str[0])
            self.progress.emit(data_str[0])
