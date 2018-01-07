import socket
from PacketHandler import PacketHandler


class ServerBase(PacketHandler):

    def __init__(self):
        PacketHandler.__init__(self)

        self.username = ""
        self.key = ""
        self.auth = False
        self.mod = "0"

    def startGameServer(self, host, port, buffer_size):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "debug:: socket opened"

        s.connect((host, port))
        print "debug:: socket server started on %s:%s" % (host, port)

        while True:
            data = s.recv(buffer_size)
            self.handlePacket(data)

    def startLoginServer(self, host, port, buffer_size):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "debug:: socket opened"

        s.connect((host, port))
        print "debug:: socket server started on %s:%s" % (host, port)

        while True:
            data = s.recv(buffer_size)
            self.handlePacket(data)
