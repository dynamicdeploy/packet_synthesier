'''
Created on Dec 10, 2012

@author: oleg
'''

from cmd import Cmd
import imp
import os
import inspect
import sys
import re
from functools import partial
from  VariableValueParser import VariableValueParser
from History import History
from History import ReadLineImpl

class Interpreter(Cmd):
    
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    BRYELLOW = '\033[93m'
    YELLOW = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    INTRO = BRYELLOW + \
'''   __
 <(\033[91mo\033[93m )___
  ( ._> /  
   `---'   
''' + ENDC
    
    def __init__(self):
        Cmd.__init__(self)
        if sys.platform.startswith("win"):
            self.__disableColors()
        
        self.__home = os.path.expanduser("~")
        self.__appDir = os.path.dirname(__file__)
        self.__historyFile = os.path.normpath(self.__home + "/.pkt_synth")
        self.__packetGenerator = None
        self.__packetSender = None
        self.__context = {}
        self.__packet_context_difference = set([])
        self.__sender_context_difference = set([])
        self.__listPacketGenerators = self.__findInheritedClasses('AbstractPacket')
        self.__listPacketSenders = self.__findInheritedClasses('AbstractSender')
        self.prompt = self.OKGREEN + ">>" + self.ENDC
        self.__valueParser = VariableValueParser(self.__context)
        
        readlineImpl = ReadLineImpl(self.__historyFile)
        self.__history = History( readlineImpl )
        self.__history.load()
        
    
    def __disableColors(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.BRYELLOW = ''
        self.YELLOW = ''
        self.FAIL = ''
        self.ENDC = ''
        self.INTRO =\
'''   __
 <(o )___
  ( ._> /  
   `---'   
'''
    
    def __findInheritedClasses(self, baseClass):
        fileExtensions = ('.py')
        definedModules = []
        allClasses = {}

        for fileInCurDir in os.listdir(self.__appDir):
            if fileInCurDir.endswith(fileExtensions):
                filename = fileInCurDir.split('.')[0]
                fp, pathname, description = imp.find_module(filename)
                module = imp.load_module(filename, fp, pathname, description)
                for name, value in inspect.getmembers(module):
                    if inspect.isclass(value):
                        if str(name).find(baseClass) == -1:
                            allClasses[name] = value
        
        for className in allClasses:
            if str(inspect.getmro(allClasses[className])).find(baseClass + ".") != -1:
                definedModules.append(className)
        return definedModules

    def saveHistory(self):
        self.__history.save()

    def cmdloop(self):
        intro = self.INTRO
        
        while(True):
            try:
                Cmd.cmdloop(self, intro)
                break
            except KeyboardInterrupt:
                self.stdout.write("\n")
                break
            except Exception:
                import traceback
                traceback.print_exc()

        self.saveHistory()   
            
    
    def do_quit(self, arg):
        return True
        
    def do_EOF(self, arg):
        return True
    
    def print_possible_load_list(self):
        print "Generators:"
        self.print_generators()
        print "Senders:"
        self.print_senders()       
    
    def print_generators(self):
        for module in self.__listPacketGenerators:
            print "\t" + module
    
    def print_senders(self):
        for module in self.__listPacketSenders:
            print "\t" + module
        
    def print_env(self, arg):
        for var in self.__context.keys():
            print self.BRYELLOW + var + self.ENDC + "=" + repr(self.__context[var])
        
    def do_export(self, arg):
        if '' == arg:
            return self.print_env(arg)
            
        eqPos = arg.find("=")
        if( -1 == eqPos):
            print "Syntax error. Please use as set var=value"
        else:
            self.__context[arg[0:eqPos].strip()] = self.parseVariableValue(arg[eqPos+1:])
    
    def do_send(self, arg):
        if '' == arg:
            arg = "1"
        
        packet = self.__packetGenerator.generatePacket();
            
        for x in range( 0, int(arg)):       
            self.__packetSender.sendPacket(packet)
            print "Sent[" + str(x) + "]:"  + repr(packet);
    
    def do_load(self, arg):
        return self.exceptSafeInvoker(partial(self.load_impl,arg))
    
    def removeItems(self, dict, keys ):
        for key in keys:
            dict.pop(key)
    
    def load_impl(self, arg):
        if arg == '':
            self.print_possible_load_list()
            return
        
        if( str(arg) in self.__listPacketGenerators):
            self.removeItems(self.__context, self.__packet_context_difference)
            contextCopy = self.__context.copy()
            self.loadGenerator(arg)
            self.__packet_context_difference = set(self.__context.keys()) - set(contextCopy.keys())
            return
        
        if( arg in self.__listPacketSenders):
            self.removeItems(self.__context, self.__sender_context_difference)
            contextCopy = self.__context.copy()
            self.loadSender(arg)
            self.__sender_context_difference = set(self.__context.keys()) - set(contextCopy.keys())
            return
        
        print arg + " is not loaded, no such module "
        
    def loadGenerator(self, arg):
        fp = None
        try:
            fp, pathname, description = imp.find_module(arg)
            module = imp.load_module(arg, fp, pathname, description)
            packetGenerator = getattr(module, arg)
            self.__packetGenerator = packetGenerator(self.__context)
            print arg + " loaded"
        except:
            import traceback
            traceback.print_exc()
            print arg + " is not loaded, no such module "
            if fp:
                fp.close()

    def loadSender(self, arg):
        fp = None
        try:
            fp, pathname, description = imp.find_module(arg)
            module = imp.load_module(arg, fp, pathname, description)
            packetSender = getattr(module, arg)
            self.__packetSender = packetSender(self.__context)
            print arg + " loaded "
        except:
            print arg + " is not loaded, no such module "
            if fp:
                fp.close()
                          
    def do_help(self, arg):
        print "\t load [sender,generator] - load available packet sender or available packet type generator"
        print "\t quit - exit application"
        print "\t send [number_of_packets_to_send] - generate and send packet"
        print "\t export [variable = value | {lambda} | {$variable} ] - setting value to a context variable"
        print "\t clobber - reset everything, besides history"
        print "\t history [[script] | [last <number>] | [clear]]"
    
    def do_clobber(self, arg):
        return self.exceptSafeInvoker(partial(self.clobber_impl,arg)) 
      
    def clobber_impl(self, arg):
        self.__packetGenerator = None
        self.__packetSender = None
        self.__context = {}
        
    def do_history(self, arg):
        return self.exceptSafeInvoker(partial(self.history_impl,arg))
    
    def printHistory(self, history):
        for item in history:
            print item
    
    def history_impl(self, arg):
        if arg.startswith("clear"):
            self.__history.clear();
            return
        
        if '' == arg:
            self.printHistory(self.__history.get(self.__history.passAllPredicate))
            return
        
        if arg.startswith('script'):
            self.printHistory(self.__history.get(self.__history.passScript))
            return
                
        if arg.startswith('last'):
            linesNumber = int(arg.replace('last', '').strip(" "))
            self.printHistory(self.__history.getLastN_lines(linesNumber))
            return
        
        print "history syntax error, please type help for more information"
        
    
    def completedefault_impl(self, predicate, all_targets, *ignored):
        if predicate(ignored[1]):
            if ignored[0] == '':
                return all_targets
            else:
                matched = []
                for target in all_targets:
                    if target.lower().startswith(ignored[0].lower()):
                        matched.append(target)
                        
                return matched
        
        return None
    
    def load_cmd_predicate(self, cmd):
        if cmd.startswith('load'):
            return True
        
        return False
    
    def export_cmd_predicate(self, cmd):
        isVariableName_LHS = (cmd.startswith('export') and cmd.find('=') == -1)
        rhsVariablePattern = re.compile(r'=\{\$')
        
        if isVariableName_LHS or (re.search(rhsVariablePattern, cmd ) is not None):
            return True
        
        return False
    
    def history_cmd_predicate(self, cmd):
        return cmd.startswith("history")
        
    def completedefault(self, *ignored):
        completation_variants =\
            self.completedefault_impl( self.load_cmd_predicate, 
                                       self.__listPacketGenerators + self.__listPacketSenders,
                                       *ignored )
        if completation_variants is not None:
            return completation_variants
        
        completation_variants =\
            self.completedefault_impl( self.export_cmd_predicate, 
                                       self.__context.keys(),
                                       *ignored )
        if completation_variants is not None:
            return completation_variants
        
        completation_variants =\
            self.completedefault_impl( self.history_cmd_predicate, 
                                       ['last', 'script', 'clear'],
                                       *ignored )
        if completation_variants is not None:
            return completation_variants
        
        return []
            
    def exceptSafeInvoker(self, functor):
        try:
            return functor()
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except ValueError:
            print "Could not convert data to an integer."
        except KeyboardInterrupt:
            return True
        except:
            import traceback
            traceback.print_exc()
        
        return None 
    
    def parseVariableValue(self, value):
        return self.__valueParser.parseVariableValue(value)    
                    
        
