from ServerBase import ServerBase


class PacketHandler(ServerBase):

    def __init__(self):
        ServerBase.__init__(self)

    def handlePacket(self, packet):
        packet = str(packet)

        if packet[0] == "<":
            print "Received XML data type!"
            self.handleXMLPacket(packet)
        elif packet[0] == "%":
            print "Received RAW data type!"
            self.handleRAWPacket(packet)
        else:
            print "Received an unknown packet: %s" % packet

    def handleRAWPacket(self, packet):
        pass

    def handleXMLPacket(self, packet):
        pass
