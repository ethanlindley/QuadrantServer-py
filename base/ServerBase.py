from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from PacketHandler import PacketHandler


class ServerBaseFactory(Factory):

    def __init__(self):
        self.users = None

    def buildProtocol(self, addr):
        return ServerBase(self.users)


class ServerBase(PacketHandler, LineReceiver):

    # TODO: properly have different states and handle as necessary

    def __init__(self, users):
        PacketHandler.__init__(self)
        self.users = users

    def connectionMade(self):
        # TODO: keep a list or array of user names and their respective UIDs
        self.users += 1

    def lineReceived(self, line):
        self.handleReceivedPacket(line)

    def __sendLine(self, line):
        self.sendLine(line)
