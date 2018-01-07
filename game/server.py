import binascii
import os
from base.ServerBase import ServerBase


class GameServer(ServerBase):

    """ main module when running the game server """

    def __init__(self):
        ServerBase.__init__(self)

        self.username = ""
        self.key = ""
        self.auth = False
        self.mod = "0"

    def startServer(self):
        host = "localhost"
        port = 6113
        buffer_size = 4096
        self.startGameServer(host, port, buffer_size)

    def handleXMLPacket(self, packet):
        # the policy file tells the client where they can connect to via sockets
        if packet == "<policy-file-request/>\0":
            self.sendPacket("<cross-domain-policy><allow-access-from domain='*' "
                            "to-ports='*' /></cross-domain-policy>\0")
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
            self.sendPacket("<msg t='sys'><body action='rndK' r='-1'><k>" + self.key + "</k></body></msg>\0")
        # this is the client logging in; we can send them an error or let them through
        elif "<msg t='sys'><body action='login' r='0'>" in packet:
            username = self.getXMLString(packet, "<nick><![CDATA[", "]]", 1)
            password = self.getXMLString(packet, "<pword><![CDATA[", "]]", 2)
            print "got new user: %s" % username
            self.auth = True
            # self.sendPacket("%xt%gs%-1%127.0.0.1:CPPL:3|127.0.0.1:6114:Moderator:2% 3;\0")
            self.sendPacket("%xt%l%-1%" + username + "%" + self.key + "%0%\0")
            # self.sendPacket("%xt%e%-1%603%\0")
        else:
            print "rogue XML packet: %s" % packet

    def handleRAWPacket(self, packet):
        if self.auth is False:
            # sometimes, the packet below can get sent too quickly
            if packet != "%xt%s%f#epfgf%-1%\0":
                print "Unauthenticated data: %s" % packet
                return
        elif self.auth is True:
            # something to do with an EPF mission
            if packet == "%xt%s%f#epfgf%-1%\0":
                self.sendPacket("%xt%epfgf%-1%0%\0")
            # client is requesting their EPF points
            elif packet == "%xt%s%f#epfgr%-1%\0":
                # TODO: properly get EPF points (currently hard set)
                self.sendPacket("%xt%epfgr%-1%0%0%\0")
            # client is requesting to join the server
            # we respond with whether or not they're a moderator
            elif "%xt%s%j#js%-1%" in packet:
                self.sendPacket("%xt%js%-1%0%1%" + self.mod + "%0%\0")
            # client is requesting their inventory
            elif packet == "%xt%s%i#gi%-1%\0":
                # TODO: properly get inventory (currently hard set)
                self.sendPacket("%xt%gi%-1%\0")
            # client is requesting their buddies
            elif packet == "%xt%s%b#gb%-1%\0":
                self.sendPacket("%xt%gb%-1%%\0")
            # client is requesting their ignore list
            elif packet == "%xt%s%n#gn%-1%\0":
                self.sendPacket("%xt%gn%-1%\0")
            # not sure what this packet is..
            # it isn't documented anywhere?
            elif packet == "%xt%s%l#mst%-1%\0":
                self.sendPacket("%xt%mst%-1%0%1\0")
            # client is retrieving "puffle player" ??
            elif packet == "%xt%s%p#pgu%-1%\0":
                self.sendPacket("%xt%pg%%$puffles%\0")
            # client is retrieving their mail (postcards)
            elif packet == "%xt%s%l#mg%-1%\0":
                self.sendPacket("%xt%mg%-1%\0")
                # %xt%mg%-1%%
                # CPL|0|12|CPL|0|63
            # client is retrieving last revision (??)
            elif packet == "%xt%s%u#glr%-1%\0":
                self.sendPacket("%xt%glr%-1%10000%\0")
            # client - server heartbeat
            elif packet == "%xt%s%u#h%1%\0":
                self.sendPacket("%xt%h%1%\0")
            # undocumented packet
            elif packet == "%xt%s%u#h%-1%\0":
                self.sendPacket("%xt%h%1%\0")
            else:
                print "Unknown RAW packet: %s" % packet

    def getXMLString(self, _input, left, right, occurrence):
        stringL = _input.index(left) + len(left)
        stringR = self.getNthString(_input, right, occurrence) + stringL
        return _input[stringL] + _input[stringR - stringL]

    def getNthString(self, string, substring, index):
        return len(string.split(substring, index).join(substring))

    def checkVersion(self, ver):
        # TODO: don't hard set the version
        if ver == "153":
            self.sendPacket("<msg t='sys'><body action='apiOK' r='0'></body></msg>\0")
        else:
            self.sendPacket("<msg t='sys'><body action='apiKO' r='0'></body></msg>\0")

    def generateKey(self):
        key = binascii.b2a_hex(os.urandom(5))
        return key

    def sendPacket(self, packet):
        print "sending packet: %s" % packet  # debug
        self.s.send(packet)


gang = GameServer()
