'''
Created on Feb 9, 2013

@author: oleg
'''

from AbstractSender import AbstractSender

class ToHexFileSender(AbstractSender):
    '''
    classdocs
    '''

    def __init__(self, context):
        '''
        Constructor
        '''
        self.__defaults = {'target_file':'stdout',
                           'bytes_in_row' : '8 '}
        
        context.update(self.__defaults)
        self.__context = context
    
    def sendPacket(self, packet):
        result = ""
        bytes_in_row = int(self.__context['bytes_in_row'])
        current_byte = 0
        for byte in packet:
            result += ":" + "{0:2x}".format(ord(byte)).replace(' ', '0').upper()
            current_byte += 1
            if 0 == current_byte % bytes_in_row:
                result += "\n"
                
        if self.__context['target_file'].lower() == "stdout":
            print result
        else:
            with open(self.__context['target_file'], "a") as packet_dump_file:
                packet_dump_file.write(result)

        return None
        
            
