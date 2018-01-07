from base.ServerBase import ServerBase


class LoginServer(ServerBase):

    def __init__(self):
        ServerBase.__init__(self)

    def startServer(self):
        self.startLoginServer()
