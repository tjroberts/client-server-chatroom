from network import Handler, poll, poll_for
import sys
from threading import Thread
from time import sleep

import time

TIMEOUT_VAL = 2  #seconds
havePingResponse = False
endTime = 0

myname = raw_input('What is your name? ')

class Client(Handler):
    
    def on_close(self):
        pass
    
    def on_msg(self, msg): #right now client is assuming server is just sending pure data, no dictionaries
        global havePingResponse
        global endTime

        #do not print ping response
        if ( msg.lower() == "ping" ):
            havePingResponse = True
            endTime = time.time() * 1000
        else:
            print("Server says " + msg)

        
host, port = 'localhost', 8888
client = Client(host, port)
client.do_send({'join': myname})

def periodic_poll():
    while 1:
        poll()
        sleep(0.05)  # seconds
                            
thread = Thread(target=periodic_poll)
thread.daemon = True  # die when the main thread dies 
thread.start()

#client.do_send({'speak': myname, 'txt': mytxt})

while 1:
    
    mytxt = sys.stdin.readline().rstrip()

    if ( mytxt.lower() == "ping" ) :
        #time ping interaction
        print("Pinging chat server, sending {} bytes.".format(sys.getsizeof("ping")));

        client.do_send({'data':mytxt}) #data key when sending data to server
                
        startTime = time.time() * 1000   #milliseconds

        #wait for response
        poll_for(TIMEOUT_VAL) # in seconds
        
        if ( (not havePingResponse) ):
            print("No response from server, timed out after {:.2} seconds.".format(time.time() - (startTime/1000)))
        else:
            print("Server responded after {} ms\n".format((endTime - startTime)))
            havePingResponse = False #reset
            
    else:
        client.do_send({'speak':myname, 'txt':mytxt}) #default interaction, just name with text		
		
		
		
		
		
		
		
		
