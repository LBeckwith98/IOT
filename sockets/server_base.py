import socket
import select
import pickle

class Server:


    def __init__(self):
        self.maxSize = 1024

        # This is the setup dict for new connections:
        self.connDict = {
            "ALARM_CLOCK": {
                "active": False,
                "conn": None,
                "selfAddr": "127.0.0.1",
                "address": "192.168.2.4",
                "port": 6400,
                "socket": None
            },
        }
        for connection in self.connDict:
            self.connDict[connection]["socket"] = socket.socket()
            self.connDict[connection]["socket"].setblocking(0)
            self.connDict[connection]["socket"].bind((self.connDict[connection]["selfAddr"], self.connDict[connection]["port"]))
        self.numConns = 0


    # For any connections no active, connect if connection is available
    # Return number of current connections
    def refreshConnection(self):
        for connection in self.connDict:
            if self.connDict[connection]["active"] is False:
                self.connDict[connection]["socket"].listen(1)
                # check to see if anyone is trying to connect
                ready = select.select([self.connDict[connection]["socket"]], [], [], .1)
                if ready[0]:
                    self.connDict[connection]["conn"], \
                        self.connDict[connection]["address"] = self.connDict[connection]["socket"].accept()

                    self.connDict[connection]["active"] = True
                    self.numConns += 1
        if self.numConns == len(self.connDict):
            return 99 #indicates fully connected
        return self.numConns


    # send in str format
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def sendTo(self, connName, msg):
        try:
            if self.connDict[connName]["active"] is False:
                return False
            self.connDict[connName]["conn"].send(bytes(msg, 'utf-8'))
            return True
        except ConnectionResetError:
            # nothing to get
            self.connDict[connName]["active"]=False
            return False

    # send pickled object
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def sendCmdTo(self, connName, cmd):
        try:
            if self.connDict[connName]["active"] is False:
                return False
            data = pickle.dumps(cmd)
            self.connDict[connName]["conn"].send(data)
            return True
        except ConnectionResetError:
            # nothing to get
            self.connDict[connName]["active"] = False
            return False

    # receive in str format
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def readStrFrom(self, connName):
        try:
            msg = self.connDict[connName]["conn"].recv(self.maxSize)
            if msg == '':  # indicates connection is closed
                self.connDict[connName]["active"] = False
        except socket.error:
            # nothing to get
            msg = ''

        return msg

    # receive pickled object
    # Failure: make as inactive, reset socket, return ''
    # Success: return message
    def readCmdFrom(self, connName):
        try:
            msg = self.connDict[connName]["conn"].recv(self.maxSize).decode('utf-8')
            if msg == '':  # indicates connection is closed
                self.connDict[connName]["active"] = False
            else:
                cmd = pickle.loads(msg)
        except socket.error:
            # nothing to get
            cmd = ''

        return cmd





