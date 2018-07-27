import socket
import pickle

class Client:

    def __init__(self):
        self.maxSize = 1024
        self.client = socket.socket()
        self.client.setblocking(0)
        self.active = False
        self.address = None
        self.port = None


    # Get connection if possible
    def connect(self, address, port):
        self.address = address
        self.port = port
        try:
            self.client.setblocking(1)
            self.client.connect((self.address,self.port))
            self.client.setblocking(0)
            self.active = True
        except:
            self.client=socket.socket()
            self.client.setblocking(0)
            self.active = False
            return False
        return True


    # if connection is not active, try to get a new one
    def refreshConnect(self):
        if self.active == False:
            try:
                self.client.connect((self.address,self.port))
                self.active = True
            except socket.error as err:
                print(err)
                self.client = socket.socket()
                self.client.setblocking(0)
                self.active=False
                return False
        return True


    # send message
    # Failure: make as inactive, reset socket, return false
    # Success: return true
    def send(self, msg):
        try:
            if self.active:
                self.client.send(bytes(msg, 'utf-8'))
        except ConnectionResetError:
            # nothing to get
            self.client = socket.socket()
            self.client.setblocking(0)
            self.active = False
            return False
        return True


    # receive in str format
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def receiveStr(self):
        try:
            msg = self.client.recv(self.maxSize).decode('utf-8')
            if msg == '':  # indicates connection is closed
                self.client=socket.socket()
                self.client.setblocking(0)
                self.active = False
        except socket.error:
            # nothing to get
            msg = ''

        return msg


    # send pickled
    # Failure: make as inactive, reset socket, return false
    # Success: return true
    def sendCmd(self, msg):
        try:
            if self.active:
                data = pickle.dumps(msg)
                self.client.send(data)
        except ConnectionResetError:
            # nothing to get
            self.client = socket.socket()
            self.client.setblocking(0)
            self.active = False
            return False
        return True


    # receive pickled
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def receiveCmd(self):
        try:
            msg = self.client.recv(self.maxSize)
            if msg == '':  # indicates connection is closed
                self.client=socket.socket()
                self.client.setblocking(0)
                self.active = False
            cmd = pickle.loads(msg)
        except socket.error:
            # nothing to get
            cmd = ''

        return cmd


# client = Client()
# print(client.connect("127.0.0.1", 12345))
