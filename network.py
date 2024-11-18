import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.20.3"
        self.port = 5553
        self.addr = (self.server, self.port)
        self.information = self.connect()

    def getInformation(self):
        return self.information

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*1))
        except:
            pass

    def send(self, data, current_player_num):
        try:
            self.client.send(pickle.dumps((data, current_player_num)))
            return pickle.loads(self.client.recv(2048*4))
        except socket.error as e:
            print(e)

