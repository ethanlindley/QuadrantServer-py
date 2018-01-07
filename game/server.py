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
