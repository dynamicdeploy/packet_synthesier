'''
Created on Dec 18, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
from EthernetPacket import EthernetPacket

class MagicPacket(AbstractPacket):
   
    def __init__(self, context):
        self.__localContext = {}
        self.__etherPacket = EthernetPacket(self.__localContext)
        
        self.__defaults = {'src_mac' : '01:02:03:04:05:06',
                           'dst_mac' : 'ff:ff:ff:ff:ff:ff'}
        
        context.update(self.__defaults)
        self.__context = context
        
    def getShortDescription(self):
        return ""

    def getOptions(self):
        return ""
    
    def __generateMAC(self, strValue):
        listOctets = strValue.split(':');
        resultMAC = ""
        for octet in listOctets:
            resultMAC += (chr(int( octet, 16)))
        return resultMAC
    
    def __generateDestMAC(self):
        return self.__generateMAC(self.__context['dst_mac'])
    
    def getFullDescription(self):
        return ""
    
    def getDefaults(self):
        return ""
    
    def setOption( self, key, value ):
        pass
    
    def __generatePayload(self):
        return "\xff" * 6 + self.__generateDestMAC() * 16
        
    def generatePacket(self):
            self.__localContext['payload'] = self.__generatePayload()
            self.__localContext['ether_type'] = '0x842'
            self.__localContext.update(self.__context)
            return self.__etherPacket.generatePacket()[0:-4]
        
        