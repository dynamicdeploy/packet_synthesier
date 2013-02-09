'''
Created on Dec 9, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
import binascii
import socket


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
        listOctets = strValue.split(':');
        resultMAC = ""
        for octet in listOctets:
            resultMAC += (chr(int( octet, 16)))
        return resultMAC
    
    def __generateSourceMAC(self):
        return self.__generateMAC(self.__context['src_mac'])
    
    def __generateDestMAC(self):
        return self.__generateMAC(self.__context['dst_mac'])
    
    def __generateTag(self):
        return ""
    
    def __generatePacketType(self):
        network_order = socket.htons(int( self.__context['ether_type'], 16))
        return (chr((network_order) & 0xff)) + (chr((network_order >> 8) & 0xff)) 
    
    def __generatePayload(self):
        return self.__context['payload']
    
    def __generateCRC(self, packet ):
        crc32value = socket.htonl(binascii.crc32(packet) & 0xffffffff)
        result = ""
        result += chr((crc32value >> 24) & 0xff)
        result += chr((crc32value >> 16) & 0xff)
        result += chr((crc32value >> 8) & 0xff)
        result += chr((crc32value) & 0xff)
        
        return result
    
    def generatePacket(self):
        resultPacket = self.__generateDestMAC() + \
                       self.__generateSourceMAC() + \
                       self.__generateTag() + \
                       self.__generatePacketType() + \
                       self.__generatePayload();
        resultPacket += self.__generateCRC( resultPacket );
        return resultPacket;
    
    