import unittest
from ArpPacket import ArpPacket

class ArpPacketTest(unittest.TestCase):

    def testGenerateArpPacketPacket(self):
        context = {}
        arpPacket = ArpPacket(context)
        expected = '\x00\x01\x08\x00\x06\x04\x00\x01\x01\x02\x03\x04\x05\x06\xc0\xa8\x00\x01\x11"3DUU\xc0\xa8\x00\x02'
        self.assertEquals(expected, arpPacket.generatePacket())
        
        
          
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()