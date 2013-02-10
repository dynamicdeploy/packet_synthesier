from AbstractPacket import AbstractPacket
from PacketSenderCommon import PacketSenderCommon

import socket

class ArpPacket(AbstractPacket):
    '''
    classdocs
    '''
    def __init__(self, context):
        
        self.__defaults = {'htype' : '0x1',
                           'ptype' : '0x800',
                           'hlen'  : '0x6',
                           'plen'  : '0x4',
                           'oper'  : '0x1',
                           'sha'   : '01:02:03:04:05:06',
                           'spa'   : '192.168.0.1',
                           'tha'   : '11:22:33:44:55:55',
                           'tpa'   : '192.168.0.2'}
        
        context.update(self.__defaults)
        self.__context = context
        self.__common = PacketSenderCommon()
    
    def getHtype(self):
        return self.__common.hexStr2int_16_networkOrder(self.__context['htype'])
    
    def getPtype(self):
        return self.__common.hexStr2int_16_networkOrder(self.__context['ptype'])
    
    def getHLen(self):
        return self.__common.hexStr2int_8_networkOrder(self.__context['hlen'])
    
    def getPLen(self):
        return self.__common.hexStr2int_8_networkOrder(self.__context['plen'])
    
    def getOp(self):
        return self.__common.hexStr2int_16_networkOrder(self.__context['oper'])
    
    def getSha(self):
        return self.__common.generateMAC(self.__context['sha'])
    
    def getSpa(self):
        return socket.inet_aton(self.__context['spa'])
    
    def getTha(self):
        return self.__common.generateMAC(self.__context['tha'])
    
    def getTpa(self):
        return socket.inet_aton(self.__context['tpa'])
    
    def generatePacket(self):
        result = ""
        result += self.getHtype() + self.getPtype() + self.getHLen() + self.getPLen() + self.getOp() + self.getSha() + self.getSpa() + self.getTha() + self.getTpa()
        
        return result