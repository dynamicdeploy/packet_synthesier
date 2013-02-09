'''
Created on Dec 9, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
import binascii
import socket


class Packet_999(AbstractPacket):
    '''
    classdocs
    '''
    def __init__(self, context):
        
        self.__defaults = {'preamble' : 'DD:DD:DD:DD:DD:DD:DD:d5',
                           'sid' : '0xe001',
                           'tag' : '',
                           'payload' : "\x80" *2}
        
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

    def generatePreamble(self, strValue):
        listOctets = strValue.split(':');
        resultPreamble = ""
        for octet in listOctets:
            resultPreamble += (chr(int( octet, 16)))
        return resultPreamble

    def __generatePreamble(self):
        return self.generatePreamble(self.__context['preamble'])

    def __generateTag(self):
        return ""

    def __generatePacketSid(self):
        network_order = socket.htons(int( self.__context['sid'], 16))
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
        resultPacket = self.__generatePreamble() + \
                       self.__generatePacketSid() + \
                       self.__generateTag() + \
                       self.__generatePayload();
        resultPacket += self.__generateCRC( resultPacket );
        
        return resultPacket;
    
    