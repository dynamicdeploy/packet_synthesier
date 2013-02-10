import binascii
import socket

class PacketSenderCommon(object):
    def generateMAC(self, strValue):
        listOctets = strValue.split(':');
        resultMAC = ""
        for octet in listOctets:
            resultMAC += (chr(int( octet, 16)))
        return resultMAC
    
    def hexStr2int_8_networkOrder(self, hexStr):
        return (chr((int( hexStr, 16)) & 0xff))
    
    def hexStr2int_16_networkOrder(self, hexStr):
        network_order = socket.htons(int( hexStr, 16))
        return (chr((network_order) & 0xff)) + (chr((network_order >> 8) & 0xff))
    
    def hexString2crc32_networkOrder(self, packet):
        crc32value = socket.htonl(binascii.crc32(packet) & 0xffffffff)
        result = ""
        result += chr((crc32value >> 24) & 0xff)
        result += chr((crc32value >> 16) & 0xff)
        result += chr((crc32value >> 8) & 0xff)
        result += chr((crc32value) & 0xff)
        
        return result
          