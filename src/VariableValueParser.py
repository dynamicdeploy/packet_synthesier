'''
Created on Dec 11, 2012

@author: oleg
'''

import re


class VariableValueParser(object):
    '''
    classdocs
    '''

    def __init__(self, context):
        self.__context = context

    def replaceHandleByPattern( self, line, patternWithEscape, patternWithouEscape, handler):
        foundMatches = re.findall(patternWithEscape, line, None)
        for matchWithEscapes in foundMatches:
            numberOfEscapesTotal = matchWithEscapes.count("\\");
            match = re.findall(patternWithouEscape, matchWithEscapes)[0]
            numberOfEscapesAsPartOfMatch = match.count("\\")

            escapesOnlyCropped = matchWithEscapes.replace(match, '').replace("\\\\", "\\")
            
            if 0 != ((numberOfEscapesTotal - numberOfEscapesAsPartOfMatch) % 2):
                escapesOnlyCropped = escapesOnlyCropped.replace("\\", '', 1)

            line = line.replace( matchWithEscapes, escapesOnlyCropped + match)
            
            if 0 == ((numberOfEscapesTotal - numberOfEscapesAsPartOfMatch) % 2):   
                line = handler( line, match )
        
        return line
    
    def replaceHexHandler( self, line, match ):
        octet = match.replace("\\x", "")
        return line.replace( match, (chr(int( octet, 16) & 0xff)))
    
    def replaceHexConstants( self, line ):
        hexValuePatternWithEscape = re.compile(r"(\\+x[\d|'abcdef']+)")
        hexValueOnlyPattern = re.compile(r"\\x[\d|'abcdef']+")
        
        return self.replaceHandleByPattern( line, hexValuePatternWithEscape, hexValueOnlyPattern, self.replaceHexHandler)
    
    def replaceLambdasHandler( self, line, match ):
        expression = match.strip("{}")
        return line.replace( match, eval(expression))
    
    def replaceLambdas( self, line ):
        lambdaConstructionPatternWithEscape = re.compile(r"(\\*\{.*\})")
        lambdaConstructionPattern = re.compile(r"(\{.*\})")
    
        return self.replaceHandleByPattern( line, lambdaConstructionPatternWithEscape, lambdaConstructionPattern, self.replaceLambdasHandler)
    
    def replaceVariableHandler(self, line, match):
        varName = match.strip("{$}")
        if varName in self.__context.keys():
            return line.replace(match, self.__context[varName])
        else:
            return line.replace(match, '')
    
    def replaceEnvironmentVariables(self, line ):
        variableConstructionPatternWithEscape = re.compile(r"(\\*\{\$.*\})")
        variableConstructionPattern = re.compile(r"(\{\$.*\})")
        
        return self.replaceHandleByPattern( line, variableConstructionPatternWithEscape, variableConstructionPattern, self.replaceVariableHandler)
    
    def parseVariableValue( self, value ):
        
        line = value.lstrip().rstrip()
        line = self.replaceEnvironmentVariables( line )
        line = self.replaceLambdas( line )
        line = self.replaceHexConstants( line )
            
        return line