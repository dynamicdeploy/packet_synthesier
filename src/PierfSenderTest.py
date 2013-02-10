import unittest
from PierfSender import PierfSender


class PierfSenderTest(unittest.TestCase):
    def testPierfXML_generation(self):
        expected=\
'''
<pierf>
  <port id="net_if" device="eth0" />
    <scene id="RAW">
      <seq repeat="1">
        <packet port="net_if">
          <raw>:10:20:30:40:50</raw>
        </packet>
      </seq>
    </scene>
    <play scene="RAW" />
</pierf>
'''

        context = {}
        sender = PierfSender(context)
        packet = "\x10\x20\x30\x40\x50\xaa\xaa\xaa\xaa"
        result = sender.generatePierfXml(
                    sender.convert2Hex(
                          sender.cutCRC32(packet)))

        self.assertEquals(expected.strip(" \n\r\t"),
                          result.strip(" \n\r\t"))
                              
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()