'''
Created on Dec 9, 2012

@author: oleg
'''
import unittest
from EthernetPacket import EthernetPacket
from Packet_999 import Packet_999
from AgregatedEthernet import AgregatedEthernet

class EthernetPacketTest(unittest.TestCase):

    def testGenerate999DefaultPacket(self):
        context = {}
        packet_999 = Packet_999(context)
        expectedPacket =   "\xDD\xDD\xDD\xDD\xDD\xDD\xDD\xd5" + \
                           "\xe0\x01" + \
                           "\x80" * 2 + \
                           "\xB2\x3B\x95\x8B";
        self.assertEquals(expectedPacket, packet_999.generatePacket())
    
    def testGenerateAgregatedEthernetDefaultPacket(self):
        context = {}
        packet_agregated_ethernet = AgregatedEthernet(context)
        expectedPacket = "\x00\x50\x43\x00\x00\x01" + \
                         "\x00\x0f\xFE\x91\xFE\xD1" + \
                         "\x92\x01" + \
                         "\x55" * 7 + "\xD5" + \
                         "\xE0\x01" + \
                         "\x00\x03\x19\x00\x03\xDE" + \
                         "\xFF" * 6 + \
                         "\x08\x06" + \
                         "\x80" * 2 + \
                         "\xB2\x47\x42\x3A" + \
                         "\x53\xB9\x6F\x64" + \
                         "\x6B\x24\x47\xEC";
        self.assertEquals(expectedPacket, packet_agregated_ethernet.generatePacket())

    def testGenerateEthernetPacket1(self):
        context = {}
        packet_ethernet = EthernetPacket(context)
        context.update ({'src_mac' : 'FF:FF:FF:FF:FF:FF',
                         'dst_mac' : '00:03:19:00:03:DE',
                         'ether_type' : '0x0806',
                         'tag' : '',
                         'payload' : "\x80" * 2})
        expectedPacket = "\x00\x03\x19\x00\x03\xDE" + \
                         "\xFF\xFF\xFF\xFF\xFF\xFF" + \
                         "\x08\x06" + \
                         "\x80\x80" + \
                         "\xB2\x47\x42\x3A";
        self.assertEquals(expectedPacket, packet_ethernet.generatePacket())
    
    def testGenerate999Packet1(self):
        context = {}
        packet_999 = Packet_999(context)
        context.update ({'preamble' : "55:55:55:55:55:55:55:D5",
                         'sid' : '0xE001',
                         'tag' : '',
                         'payload' : "\x00\x03\x19\x00\x03\xDE" + \
                                     "\xFF" * 6 + \
                                     "\x08\x06" + \
                                     "\x80" * 2 + \
                                     "\xB2\x47\x42\x3A"})
        expectedPacket = "\x55" * 7 + "\xD5" + \
                         "\xE0\x01" + \
                         "\x00\x03\x19\x00\x03\xDE" + \
                         "\xFF" * 6 + \
                         "\x08\x06" + \
                         "\x80" * 2 + \
                         "\xB2\x47\x42\x3A" + \
                         "\x53\xB9\x6F\x64";
        self.assertEquals(expectedPacket, packet_999.generatePacket())
    def testGenerateEthernetPacket2(self):
        context = {}
        ethernetPacket = EthernetPacket(context)
        context.update ({'src_mac' : '00:0F:FE:91:FE:D1',
                         'dst_mac' : '00:50:43:00:00:01',
                         'ether_type' : '0x9201',
                         'tag' : '',
                         'payload' : "\x55" * 7 + "\xD5" + \
                                     "\xE0\x01" + \
                                     "\x00\x03\x19\x00\x03\xDE" + \
                                     "\xFF" * 6 + \
                                     "\x08\x06" + \
                                     "\x80" * 2 + \
                                     "\xB2\x47\x42\x3A" + \
                                     "\x53\xB9\x6F\x64"})
        expectedPacket = "\x00\x50\x43\x00\x00\x01" + \
                         "\x00\x0f\xFE\x91\xFE\xD1" + \
                         "\x92\x01" + \
                         "\x55" * 7 + "\xD5" + \
                         "\xE0\x01" + \
                         "\x00\x03\x19\x00\x03\xDE" + \
                         "\xFF" * 6 + \
                         "\x08\x06" + \
                         "\x80" * 2 + \
                         "\xB2\x47\x42\x3A" + \
                         "\x53\xB9\x6F\x64" + \
                         "\x6B\x24\x47\xEC"
        self.assertEquals(expectedPacket, ethernetPacket.generatePacket())
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()