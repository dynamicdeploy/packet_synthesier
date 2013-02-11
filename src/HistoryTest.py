import unittest

from History import History
from History import ReadLine
from mock import MagicMock

class HistoryTest(unittest.TestCase):
    
    def testPredicateAll(self):
        historyBuffer=['load smth',
                       'export aa=cc',
                       'history clear']
        
        expected=['load smth','export aa=cc']
        
        readLine = ReadLine()
        readLine.getLineBuffer = MagicMock(return_value=historyBuffer)
        
        history = History( readLine )
        result = history.get( history.passAllPredicate )
        
        self.assertEquals(expected, result)
        
    def testPredicateScript(self):
        historyBuffer=['load smth',
                       'export aa=cc',
                       'export',    
                       'export', 
                       'export',
                       'history clear']
        
        expected=['load smth','export aa=cc']
        
        readLine = ReadLine()
        readLine.getLineBuffer = MagicMock(return_value=historyBuffer)
        
        history = History( readLine )
        result = history.get( history.passScript )
        
        self.assertEquals(expected, result)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()