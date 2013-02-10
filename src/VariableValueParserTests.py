'''
Created on Dec 11, 2012

@author: oleg
'''
import unittest
from  VariableValueParser import VariableValueParser

class VariableValueParserTests(unittest.TestCase):

    def testSimpleLine(self):
        parser = VariableValueParser({})
        self.assertEquals("line", parser.parseVariableValue("line"))
    
    def testLineWithSpacesOnSides(self):
        parser = VariableValueParser({})
        self.assertEquals("line", parser.parseVariableValue("  line "))
        
    def testLineWithSpacesOnMiddle(self):
        parser = VariableValueParser({})
        self.assertEquals("l   ine", parser.parseVariableValue("l   ine"))
        
    def testLineWithBinary(self):
        parser = VariableValueParser({})
        self.assertEquals("\x80", parser.parseVariableValue(r'\x80'))
        
    def testLineWithTextAndBinary(self):
        parser = VariableValueParser({})
        self.assertEquals("A \x10", parser.parseVariableValue(r'A \x10'))
    
    def testBigValueAsOctet(self):
        parser = VariableValueParser({})
        self.assertEquals("\x10\x20\x3a\xa4\x50\x60\x70\x80\x90\x100\xaa\xbb\xcc\xdd",
                          parser.parseVariableValue(r'\x10\x20\x3a\xa4\x50\x60\x70\x80\x90\x100\xaa\xbb\xcc\xdd'))
    
    def testStringMultiplication(self):
        parser = VariableValueParser({})
        self.assertEquals( "aa" + "\x80" * 10 + "aa",
                          parser.parseVariableValue(r'aa{"\x80" * 10}aa'))
   
    def testEscapeWithHex(self):
        parser = VariableValueParser({})
        self.assertEquals(r'\x10',
                          parser.parseVariableValue(r'\\x10'))
  
    def testEscapeWithHexWihtManyEscapes(self):
        parser = VariableValueParser({})
        self.assertEquals(r'\\x10',
                          parser.parseVariableValue(r'\\\\x10'))
        
    def testEscapeWithLambda(self):
        parser = VariableValueParser({})
        self.assertEquals( "aa{\x80 * 10}aa",
                          parser.parseVariableValue(r'aa\{\x80 * 10}aa'))

    def testEnvironmentVariableInsert(self):
        parser = VariableValueParser({'var':'value'})
        self.assertEquals( "value",
                            parser.parseVariableValue("{$var}"))

    
    def testEnvironmentVariableEmptyInsert(self):
        parser = VariableValueParser({})
        self.assertEquals( '',
                          parser.parseVariableValue("{$var}"))
    
    def testEnvironmentVariableInsertInText(self):
        parser = VariableValueParser({'var':'value'})
        self.assertEquals( 'aaa-value-aaa',
                          parser.parseVariableValue("aaa-{$var}-aaa"))


    def testEscapeLambdaInNetworkInterfaceName(self):
        parser = VariableValueParser({})
        self.assertEquals( r'\Device\NPF_{20305688-5F6A-4A7A-AF1C-1BD8639165A6}',
                          parser.parseVariableValue(r"\Device\NPF_\{20305688-5F6A-4A7A-AF1C-1BD8639165A6}"))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()