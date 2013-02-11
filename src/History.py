import re

class ReadLine(object):
    
    def getLineBuffer(self):
        pass
    
    def clear(self):
        pass
    
    def readHistoryFile(self):
        pass
    
    def writeHistoryFile(self):
        pass

class ReadLineImpl(ReadLine):
    
    def __init__(self, historyFile):
        self.__historyFile = historyFile
    
    def getLineBuffer(self):
        try:
            import readline
            result = []
            for i in range(readline.get_current_history_length()):
                item = readline.get_history_item(i)
                if item is not None:
                    result.append(item)
                
            return result
        except:
            return []
    
    def clear(self):
        try:
            import readline
            return readline.clear_history()
        except:
            pass
    
    def readHistoryFile(self):
        try:
            import readline
            readline.read_history_file(self.__historyFile)
        except:
            pass
    
    def writeHistoryFile(self):
        try:
            import readline
            readline.write_history_file(self.__historyFile)
        except:
            pass


class History(object):
    def __init__(self, readLine):
        self.__readLine = readLine
    
    def get(self, filterPredicate):
        history = self.__readLine.getLineBuffer()
        result = []
  
        for item in history:
            if filterPredicate(item):
                result.append(item)
                
        return result
    
    def load(self):
       self.__readLine.readHistoryFile()
       
    def save(self):
        self.__readLine.writeHistoryFile()
        
    def clear(self):
        self.__readLine.clear()
        
    def passAllPredicate(self, item):
        allExceptHistoryCmdsPattern = re.compile(r"^history\.*")
        if re.match( allExceptHistoryCmdsPattern, item ) is not None:
            return False
        
        return True
    
    def passScript(self, item):
        if not self.passAllPredicate(item):
            return False
        
        allExceptExportWithoutArguments = re.compile(r"^export\s*$")
        if re.match( allExceptExportWithoutArguments, item):
            return False
        
        return True
    
    def getLastN_lines(self, nLastLines):
        history = self.get( self.passAllPredicate )
        return history[len(history) - nLastLines:]
        