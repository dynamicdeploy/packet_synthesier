'''
Created on Dec 9, 2012

@author: oleg
'''
from AbstractPacket import AbstractPacket
from PacketSenderCommon import PacketSenderCommon
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
        return self.__common.hexStr2int_16_networkOrder(self.__context['sid'])
    

    def __generatePayload(self):
        return self.__context['payload']

    def __generateCRC(self, packet ):
        return self.__common.hexString2crc32_networkOrder(packet)
    
    def generatePacket(self):
        resultPacket = self.__generatePreamble() + \
                       self.__generatePacketSid() + \
                       self.__generateTag() + \
                       self.__generatePayload();
        resultPacket += self.__generateCRC( resultPacket );
        
        return resultPacket;
    
    