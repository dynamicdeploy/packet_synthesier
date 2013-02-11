import unittest
from  PacketSenderCommon import PacketSenderCommon
import re

class PacketSenderCommonTests(unittest.TestCase):
    def str2int(self, strValue ):
        stripped = strValue.strip(" \r\n\t").lower()
        if stripped.startswith('0x'):
            return int(stripped, 16)
        
        if stripped.startswith('0b'):
            return int(stripped, 2)
        
        if stripped.startswith('0o'):
            return int(stripped, 8)
        
        return int(strValue)
    
    def testStrToInt(self):
        self.assertEquals(0x16, self.str2int('0x016'))
        self.assertEquals(3, self.str2int('0b11'))
        self.assertEquals(8, self.str2int('0o10'))
        self.assertEquals(10, self.str2int('10'))





if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()