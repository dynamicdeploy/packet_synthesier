'''
Created on Feb 9, 2013

@author: oleg
'''
from AbstractSender import AbstractSender

class ToVarSender(AbstractSender):
    '''
    classdocs
    '''


    def __init__(self, context):
        '''
        Constructor
        '''
        self.__defaults = {'target_var':'packet_dump' }
        
        context.update(self.__defaults)
        self.__context = context
    
    def sendPacket(self, packet):
        self.__context[self.__context['target_var']] = packet

        return None
        