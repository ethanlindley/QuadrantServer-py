import os
import binascii
import socket
import sys


class LoginServer:

    """ main login module for login server base """

    def __init__(self):
        self.key = ""
        self.s = None

        self.startServer()

    def startServer(self):
        host = ""
        port = 6112
        recv_buffer = 4096
        connections = []

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print "socket created"  # debug
        # let's bind the socket to our desired host and port
        try:
            self.s.bind((host, port))
        except socket.error as msg:
            print "server failed to initialize... message: %s" % msg
            sys.exit()
        print "successfully initialized the server"

        self.s.listen(10)  # let's start listening on the socket

        # let's continue communicating with the client
        sockfd, addr = self.s.accept()
        while True:
            for sock in connections:
                # handle new connection
                if sock == self.s:
                    # handle the case in which there is a new connection received through the server socket
                    connections.append(sockfd)
                    print "client (%s, %s) has connected" % (sockfd, addr)
                # let's handle an incoming message from a client
                else:
                    try:
                        data = sock.recv(recv_buffer)
                        self.handlePacket(data)
                    except:
                        print "client (%s, %s) has disconnected" % (sockfd, addr)
                        sock.close()
                        connections.remove(sock)
                        continue

    def handlePacket(self, packet):
        if packet == "<policy-file-request/>\0":
            self.sendPacket("<cross-domain-policy><allow-access-from domain='*' "
                            "to-ports='*' /></cross-domain-policy>\0")
        elif "<msg t='sys'><body action='verChk'" in packet:
            version = self.getXMLString(packet, "<ver v='", "'", 8)
            self.checkVersion(version)
        elif packet == "<msg t='sys'><body action='rndK' r='-1'></body></msg>\0":
            self.key = self.generateKey()
            self.sendPacket("<msg t='sys'><body action='rndK' r='-1'><k>" + self.key + "</k></body></msg>\0")
        elif "<msg t='sys'><body action='login' r='0'>" in packet:
            username = self.getXMLString(packet, "<nick><![CDATA[", "]]", 1)
            password = self.getXMLString(packet, "<pword><![CDATA[", "]]", 2)
            print "got new user: %s" % username
            # self.sendPacket("%xt%gs%-1%127.0.0.1:CPPL:3|127.0.0.1:6114:Moderator:2% 3;\0")
            self.sendPacket("%xt%gs%-1%127.0.0.1:6113:CPPL:3% 3;\0")
            self.sendPacket("%xt%l%-1%" + username + "%" + self.key + "%0%\0")
            # self.sendPacket("%xt%e%-1%603%\0")
        else:
            print "rogue packet: %s" % packet

    def checkVersion(self, ver):
        # TODO: don't hard set the version
        if ver == "153":
            self.sendPacket("<msg t='sys'><body action='apiOK' r='0'></body></msg>\0")
        else:
            self.sendPacket("<msg t='sys'><body action='apiKO' r='0'></body></msg>\0")

    def generateKey(self):
        key = binascii.b2a_hex(os.urandom(5))
        return key

    def getXMLString(self, _input, left, right, occurrence):
        stringL = _input.index(left) + len(left)
        stringR = self.getNthString(_input, right, occurrence) + stringL
        return _input[stringL] + _input[stringR - stringL]

    def getNthString(self, string, substring, index):
        return len(string.split(substring, index).join(substring))

    def sendPacket(self, packet):
        print "sending packet: %s" % packet  # debug
        self.s.send(packet)


gang = LoginServer()
