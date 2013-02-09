packet_synthesier
=================

CLI tool for generation different types of network packets

Note: No garantie to work on WinX with RawSender

Description:

The cli operates with 3 types of objects.
1. Generators  - modules for generate packet of specific type
2. Senders     - modules for send packets, raw socket, file e.t.c
3. Variables   - user should setup Senders and Generators by setting internal environment
                 variables

Short HOW TO:

To run script please type in the packet_synthesier folder
Note: raw socket request root privilegies

sudo python ./src/main.py 

You'll see the greeting message
   __
 <(o )___
  ( ._> /  
   `---'   

>>

Type: load EthernetPacket
Type: export

You'll see the internal environment:

dst_mac='01:02:03:04:05:06'
tag=''
ether_type='0x801'
payload='\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
src_mac='01:02:03:04:05:06'

Type: export dst_mac=ff:ff:ff:ff:ff:ff
Type: export

dst_mac='ff:ff:ff:ff:ff:ff'
tag=''
ether_type='0x801'
payload='\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80\x80'
src_mac='01:02:03:04:05:06'

Ok, the destination MAC changed.

Type: export payload={"\xab" * 32}
Type: export

dst_mac='ff:ff:ff:ff:ff:ff'
tag=''
ether_type='0x801'
payload='\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab\xab'
src_mac='01:02:03:04:05:06'

Type: load RawSender
Type: send 4

Ok, 4 ethernet packet generated and sent.

Detail description:

- Click tab twice to get list of all commands

- export    Without arguments prints internal environment
            To set variable use following syntax:
            
            export [var_name]=[[string][lambda][variable]]
            	string: hello-world \xaa\xbb\xcc
            	lambda: {<python commands>}
            	variable: {$<var_name>}

            Examples:
            	export foo = bar
            Or:
            	export foo1 = {"\x10" * 20}

            Or:
                export foo2 = {$foo1}\xcc\xcc\xcc\xaa

            Note: auto-completation supports variables

- load    	Without arguments it prints possible modules to load.
 			
 			load [module_name]

 			Example:

 				load RawSender


- send 		Sends packet with current sender
			send [number_of_packets_to_send]

			Example:
				send 10

How to add custom sender:
	1. create python module with same name class (case sensitive)
	2. from AbstractSender import AbstractSender
	3. inherit  new sender class from AbstractSender
	4. implement  def __init__(self, context)
	5. implement def sendPacket(self, packet):
	6. place new module to packet_synthesier/src

How to add custom packet generator:
	1. create python module with same name class (case sensitive)
	2. from AbstractPacket import AbstractPacket
	3. inherit  new sender class from AbstractPacket
	4. implement  def __init__(self, context)
	5. implement def generatePacket(self):
	6. place new module to packet_synthesier/src
	

