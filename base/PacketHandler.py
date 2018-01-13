from utils.PacketTypes import *
import logging


class PacketHandler(object):

    # TODO: properly handle packets and send them to the client

    def __init__(self):
        self.logger = logging.Logger("PacketHandler")

    def handleReceivedPacket(self, packet):
        packet = str(packet)

        if packet[0] == "<":
            self.logger.debug("received XML packet with data: %s") % packet
            self.handleXMLPacket(packet)
        elif packet[0] == "%":
            self.logger.debug("received RAW packet with data: %s") % packet
            self.handleRAWPacket(packet)

    def handleXMLPacket(self, packet):
        pass

    def handleRAWPacket(self, packet):
        pass
