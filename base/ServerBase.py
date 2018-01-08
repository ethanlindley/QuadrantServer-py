from PacketHandler import PacketHandler
import socket

"""
MIT License

Copyright (c) 2018 Ethan Lindley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class ServerBase(PacketHandler):

    def __init__(self):
        PacketHandler.__init__(self)

    def startGameServer(self, host, port):

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
            self.setup(conn)
            self.handlePacket(data)
            conn.close()

    def startLoginServer(self, host, port):

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
            self.setup(conn)
            self.handlePacket(data)
            conn.close()
