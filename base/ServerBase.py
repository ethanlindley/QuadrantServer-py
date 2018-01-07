from PacketHandler import PacketHandler
import socket


class ServerBase(PacketHandler):

    def __init__(self):
        PacketHandler.__init__(self)

    def startGameServer(self):
        host = None
        port = 6113

        for socket_information in socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM):
            family, _type, prototype, name, socket_address = socket_information

        s = socket.socket(family, _type, prototype)
        print "debug:: binding login server..."
        s.bind(socket_address)
        print "debug:: login server now listening on port %s" % port
        s.listen(10000)

        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            self.handlePacket(data)
            conn.close()

    def startLoginServer(self):
        host = None
        port = 6112

        for socket_information in socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM):
            family, _type, prototype, name, socket_address = socket_information

        s = socket.socket(family, _type, prototype)
        print "debug:: binding login server..."
        s.bind(socket_address)
        print "debug:: login server now listening on port %s" % port
        s.listen(10000)

        while True:
            conn, addr = s.accept()
            data = conn.recv(1024)
            self.handlePacket(data)
            conn.close()
