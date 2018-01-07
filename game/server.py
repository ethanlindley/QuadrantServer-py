from base.ServerBase import ServerBase


class GameServer(ServerBase):

    def __init__(self):
        ServerBase.__init__(self)

    def startServer(self):
        self.startGameServer()
