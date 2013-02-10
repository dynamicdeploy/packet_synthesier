

from AbstractSender import AbstractSender
import tempfile
import subprocess
import os

class PierfSender(AbstractSender):
    '''
    classdocs
    '''
    pierfXML_template =\
'''
<pierf>
  <port id="net_if" device="{0}" />
    <scene id="RAW">
      <seq repeat="1">
        <packet port="net_if">
          <raw>{1}</raw>
        </packet>
      </seq>
    </scene>
    <play scene="RAW" />
</pierf>
'''
    def __init__(self, context):
        '''
        Constructor
        '''
        self.__defaults = {'interface':'eth0',
                           'pierf_app_full_file_name' : '/opt/pierf/pierf'}
        
        context.update(self.__defaults)
        self.__context = context
    
    def cutCRC32(self, packet ):
        return  packet[0:-4]
    
    def convert2Hex(self, packet ):
        result = ""
        for byte in packet:
            result += ":" + "{0:2x}".format(ord(byte)).replace(' ', '0').upper()
        
        return result
    
    def generatePierfXml(self, hexPacket):
        pierfXML = self.pierfXML_template.format(self.__context['interface'], 
                                            hexPacket)
        return pierfXML
    
    def runPierf(self, configFileName):
        subprocess.call([self.__context['pierf_app_full_file_name'],configFileName])
    
    def sendPacket(self, packet):    
        try:
            tmpFileName = None
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpFile:
                tmpFile.write( 
                    self.generatePierfXml(
                        self.convert2Hex(
                            self.cutCRC32(packet))))
                
                tmpFile.flush()
                tmpFileName = tmpFile.name
            
            self.runPierf(tmpFileName)
        finally:
            if tmpFileName:
                os.unlink(tmpFileName)

            
        return None