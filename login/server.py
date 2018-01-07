from base.ServerBase import ServerBase


class LoginServer(ServerBase):

    """ main login module for login server base """

    def __init__(self):
        ServerBase.__init__(self)

        self.key = ""
        self.s = None

        self.startServer()

    def startServer(self):
        host = "localhost"
        port = 6112
        buffer_size = 4096
        self.startLoginServer(host, port, buffer_size)
