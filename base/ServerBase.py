from PacketHandler import PacketHandler


class ServerBase(PacketHandler):

    def __init__(self):
        PacketHandler.__init__(self)

    def startGameServer(self):
        host = ""
        port = 6113

    def startLoginServer(self):
        host = ""
        port = 6112
