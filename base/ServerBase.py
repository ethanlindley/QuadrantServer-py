import socket
import binascii
import os
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
        print "debug:: game socket opened"

        s.connect((host, port))
        print "debug:: game socket server started on %s:%s" % (host, port)

        while True:
            data = s.recv(buffer_size)
            self.handlePacket(data)

    def startLoginServer(self, host, port, buffer_size):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print "debug:: login socket opened"

        s.connect((host, port))
        print "debug:: login socket server started on %s:%s" % (host, port)

        while True:
            data = s.recv(buffer_size)
            self.handlePacket(data)

    def generateKey(self):
        key = binascii.b2a_hex(os.urandom(5))
        return key

    def checkVersion(self, ver):
        # TODO: don't hard set the version
        if ver == "153":
            self.sendPacket("<msg t='sys'><body action='apiOK' r='0'></body></msg>\0")
        else:
            self.sendPacket("<msg t='sys'><body action='apiKO' r='0'></body></msg>\0")
