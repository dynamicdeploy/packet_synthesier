'''
Created on Dec 9, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
import imp


class AgregatedEthernet(AbstractPacket):
    '''
    classdocs
    '''
    def __init__(self, context):
        self.__eth0PacketGenerator = None
        self.__eth1PacketGenerator = None
        self.__999PacketGenerator = None
        self.__defaults = {'dst_mac_level0' : '00:50:43:00:00:01',
                           'src_mac_level0' : '00:0f:fe:91:fe:d1',
                           'ether_type_level0' : '0x9201',
                           'ether_tag_level0' : '',
                           'ether_payload_level0' : "\x80" * 42,
                           'preamble_999' : "55:55:55:55:55:55:55:D5",
                           'sid999' : '0xE001',
                           'tag999' : '',
                           'dst_mac_level1' : '00:03:19:00:03:DE',
                           'src_mac_level1' : 'FF:FF:FF:FF:FF:FF',
                           'ether_type_level1' : '0x0806',
                           'ether_tag_level1' : '',
                           'ether_payload_level1' : "\x80" * 2}

        context.update(self.__defaults)
        self.__context = context
        self.__ethLevel0Context = {}
        self.__ethLevel1Context = {}
        self.__999Context = {}

    def getShortDescription(self):
        return ""

    def getOptions(self):
        return ""

    def getFullDescription(self):
        return ""

    def getDefaults(self):
        return ""

    def setOption( self, key, value ):
        pass
    
    def __loadEthernetModuleLevel0(self):
        fp, pathname, description = imp.find_module('EthernetPacket')
        try:
            module = imp.load_module('EthernetPacket', fp, pathname, description)
            packetGenerator = getattr(module, 'EthernetPacket')
            self.__eth0PacketGenerator = packetGenerator(self.__ethLevel0Context)
            print 'EthernetPacket' + " loaded"
        finally:
            if fp:
                fp.close()

    def __loadEthernetModuleLevel1(self):
        fp, pathname, description = imp.find_module('EthernetPacket')
        try:
            module = imp.load_module('EthernetPacket', fp, pathname, description)
            packetGenerator = getattr(module, 'EthernetPacket')
            self.__eth1PacketGenerator = packetGenerator(self.__ethLevel1Context)
            print 'EthernetPacket' + " loaded"
        finally:
            if fp:
                fp.close()
    
    def __load999Module(self):
        fp, pathname, description = imp.find_module('Packet_999')
        try:
            module = imp.load_module('Packet_999', fp, pathname, description)
            packetGenerator = getattr(module, 'Packet_999')
            self.__999PacketGenerator = packetGenerator(self.__999Context)
            print 'Packet_999' + " loaded"
        finally:
            if fp:
                fp.close()
    
    def generatePacket(self):
        self.__loadEthernetModuleLevel0()
        self.__loadEthernetModuleLevel1()
        self.__load999Module()
        self.__ethLevel1Context.update({'src_mac' : self.__context['src_mac_level1'],
                                        'dst_mac' : self.__context['dst_mac_level1'],
                                        'ether_type' : self.__context['ether_type_level1'],
                                        'tag' : self.__context['ether_tag_level1'],
                                        'payload' : self.__context['ether_payload_level1']})
        ethPacketLevel1 = self.__eth1PacketGenerator.generatePacket()
        self.__999Context.update({'preamble' : self.__context['preamble_999'],
                                  'sid' : self.__context['sid999'],
                                  'tag' : self.__context['tag999'],
                                  'payload' : ethPacketLevel1})
        Packet999 = self.__999PacketGenerator.generatePacket()
        self.__ethLevel0Context.update({'src_mac' : self.__context['src_mac_level0'],
                                        'dst_mac' : self.__context['dst_mac_level0'],
                                        'ether_type' : self.__context['ether_type_level0'],
                                        'tag' : self.__context['ether_tag_level0'],
                                        'payload' : Packet999})
        ethPacketLevel0 = self.__eth0PacketGenerator.generatePacket()
        return ethPacketLevel0

