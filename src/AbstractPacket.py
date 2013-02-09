'''
Created on Dec 9, 2012

@author: oleg
'''

class AbstractPacket(object):
    '''
    classdocs
    '''

    def __init__(self):
        pass 

    def getShortDescription(self):
        return None

    def getFullDescription(self):
        return None

    def getOptions(self):
        return None

    def getDefaults(self):
        return None

    def setOption( self, key, value ):
        pass

    def generatePacket(self):
        return None