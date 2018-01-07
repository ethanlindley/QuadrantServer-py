import socket
import os
import binascii

"""
MIT License

Copyright (c) 2018 Ethan Lindley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class PacketHandler:

    def __init__(self):
        self.mod = "0"
        self.auth = False
        self.username = ""
        self.key = ""

    def handlePacket(self, packet):
        packet = str(packet)

        if packet[0] == "%":
            print "Received RAW data type!"
            print packet  # debug
            self.handleRAWPacket(packet)
        elif packet[0] == "<":
            print "Received XML data type!"
            print packet  # debug
            self.handleXMLPacket(packet)
        else:
            print "Received an unknown packet: %s" % packet

    def handleRAWPacket(self, packet):
        if self.auth is False:
            # sometimes, the packet below can get sent too quickly
            if packet != "%xt%s%f#epfgf%-1%\0":
                print "Unauthenticated data: %s" % packet
                return
        elif self.auth is True:
            # something to do with an EPF mission
            if packet == "%xt%s%f#epfgf%-1%\0":
                self.sendPacket("%xt%epfgf%-1%0%\0", 6113)
            # client is requesting their EPF points
            elif packet == "%xt%s%f#epfgr%-1%\0":
                # TODO: properly get EPF points (currently hard set)
                self.sendPacket("%xt%epfgr%-1%0%0%\0", 6113)
            # client is requesting to join the server
            # we respond with whether or not they're a moderator
            elif "%xt%s%j#js%-1%" in packet:
                self.sendPacket("%xt%js%-1%0%1%" + self.mod + "%0%\0", 6113)
            # client is requesting their inventory
            elif packet == "%xt%s%i#gi%-1%\0":
                # TODO: properly get inventory (currently hard set)
                self.sendPacket("%xt%gi%-1%\0", 6113)
            # client is requesting their buddies
            elif packet == "%xt%s%b#gb%-1%\0":
                self.sendPacket("%xt%gb%-1%%\0", 6113)
            # client is requesting their ignore list
            elif packet == "%xt%s%n#gn%-1%\0":
                self.sendPacket("%xt%gn%-1%\0", 6113)
            # not sure what this packet is..
            # it isn't documented anywhere?
            elif packet == "%xt%s%l#mst%-1%\0":
                self.sendPacket("%xt%mst%-1%0%1\0", 6113)
            # client is retrieving "puffle player" ??
            elif packet == "%xt%s%p#pgu%-1%\0":
                self.sendPacket("%xt%pg%%$puffles%\0", 6113)
            # client is retrieving their mail (postcards)
            elif packet == "%xt%s%l#mg%-1%\0":
                self.sendPacket("%xt%mg%-1%\0", 6113)
                # %xt%mg%-1%%
                # CPL|0|12|CPL|0|63
            # client is retrieving last revision (??)
            elif packet == "%xt%s%u#glr%-1%\0":
                self.sendPacket("%xt%glr%-1%10000%\0", 6113)
            # client - server heartbeat
            elif packet == "%xt%s%u#h%1%\0":
                self.sendPacket("%xt%h%1%\0", 6113)
            # undocumented packet
            elif packet == "%xt%s%u#h%-1%\0":
                self.sendPacket("%xt%h%1%\0", 6113)
            else:
                print "Unknown RAW packet: %s" % packet

    def handleXMLPacket(self, packet):
        # the policy file tells the client where they can connect to via sockets
        if packet == "<policy-file-request/>\0":
            self.sendPacket(
                "<cross-domain-policy><allow-access-from domain='*' to-ports='*' /></cross-domain-policy>\0", 6112)
        # we receive the version of the client and then we compare it with what it should be
        # we reply with OK if the version checks out and KO if it does not
        elif "<msg t='sys'><body action='verChk'" in packet:
            ver = self.getXMLString(packet, "<ver v='", "'", 8)
            self.checkVersion(ver)
        # this is the client asking for a random key to salt their hashed password
        # we store the key so that we can pull the hashed password out of the db,
        # salt it with the key, and then compare them
        elif packet == "<msg t='sys'><body action='rndK' r='-1'></body></msg>\0":
            self.key = self.generateKey()
            self.sendPacket("<msg t='sys'><body action='rndK' r='-1'><k>" + self.key + "</k></body></msg>\0", 6112)
        # this is the client logging in; we can send them an error or let them through
        elif "<msg t='sys'><body action='login' r='0'>" in packet:
            username = self.getXMLString(packet, "<nick><![CDATA[", "]]", 1)
            password = self.getXMLString(packet, "<pword><![CDATA[", "]]", 2)
            print "got new user: %s" % username
            self.auth = True
            # self.sendPacket("%xt%gs%-1%127.0.0.1:CPPL:3|127.0.0.1:6114:Moderator:2% 3;\0")
            self.sendPacket("%xt%l%-1%" + username + "%" + self.key + "%0%\0", 6112)
            # self.sendPacket("%xt%e%-1%603%\0")
        else:
            print "rogue XML packet: %s" % packet

    def sendPacket(self, packet, port):
        host = socket.gethostbyname("localhost")
        addr = (host, port)

        # let's open the socket and connect to the desired server
        # packet will either be sent to login or game server depending on args passed through
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(addr)
        s.send(packet)
        # finally, let's close the socket as we don't need it any more until we need to send another
        # packet to the server
        s.close()

    def getXMLString(self, _input, left, right, occurrence):
        stringL = _input.index(left) + len(left)
        stringR = self.getNthString(_input, right, occurrence) + stringL
        return _input[stringL] + _input[stringR - stringL]

    def getNthString(self, string, substring, index):
        return len(string.split(substring, index).join(substring))

    def generateKey(self):
        key = binascii.b2a_hex(os.urandom(5))
        return key

    def checkVersion(self, ver):
        # TODO: don't hard set the version
        if ver == "153":
            self.sendPacket("<msg t='sys'><body action='apiOK' r='0'></body></msg>\0", 6112)
        else:
            self.sendPacket("<msg t='sys'><body action='apiKO' r='0'></body></msg>\0", 6112)
