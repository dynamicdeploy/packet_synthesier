'''
Created on Dec 9, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
from PacketSenderCommon import PacketSenderCommon

class EthernetPacket(AbstractPacket):
    '''
    classdocs
    '''
    def __init__(self, context):
        
        self.__defaults = {'src_mac' : '01:02:03:04:05:06',
                           'dst_mac' : '01:02:03:04:05:06',
                           'ether_type' : '0x801',
                           'tag' : '',
                           'payload' : "\x80" * 42}
        
        context.update(self.__defaults)
        self.__context = context
        self.__common = PacketSenderCommon()
        
    def getShortDescription(self):
        return ""

    def getOptions(self):
        return ""

    def getFullDescription(self):
        return ""

    def getDefaults(self):
        return ""

    def setOption( self, key, value ):
        pass
    
    def __generateMAC(self, strValue):
        return self.__common.generateMAC(strValue)
    
    def __generateSourceMAC(self):
        return self.__generateMAC(self.__context['src_mac'])
    
    def __generateDestMAC(self):
        return self.__generateMAC(self.__context['dst_mac'])
    
    def __generateTag(self):
        return ""
    
    def __generatePacketType(self):
        return self.__common.hexStr2int_16_networkOrder(self.__context['ether_type'])
    
    def __generatePayload(self):
        return self.__context['payload']
    
    def __generateCRC(self, packet ):
        return self.__common.hexString2crc32_networkOrder(packet)
    
    def generatePacket(self):
        resultPacket = self.__generateDestMAC() + \
                       self.__generateSourceMAC() + \
                       self.__generateTag() + \
                       self.__generatePacketType() + \
                       self.__generatePayload();
        resultPacket += self.__generateCRC( resultPacket );
        return resultPacket;
    
    