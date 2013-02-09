'''
Created on Dec 10, 2012

@author: oleg
'''

from AbstractSender import AbstractSender

class RawSender(AbstractSender):
    '''
    classdocs
    '''

    def __init__(self, context):
        '''
        Constructor
        '''
        self.__defaults = {'interface':'eth0'}
        
        context.update(self.__defaults)
        self.__context = context
    
    def sendPacket(self, packet):
        from socket import socket, AF_PACKET, SOCK_RAW
        s = socket(AF_PACKET, SOCK_RAW)
        s.bind((self.__context['interface'], 0))
        s.send( packet[0:-4] )
        return None