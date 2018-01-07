from login.server import LoginServer


class StartLoginServer(LoginServer):

    def __init__(self):
        LoginServer.__init__(self)
        print "debug:: starting login server..."
        self.startLoginServer()


login = StartLoginServer()

