from game.server import GameServer


class StartGameServer(GameServer):

    def __init__(self):
        GameServer.__init__(self)
        print "debug:: starting game server..."
        self.startServer()


game = StartGameServer()
