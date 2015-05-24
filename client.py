from network import Handler, poll, poll_for
import sys
from threading import Thread
from time import sleep

import time

#could delcare all relevant data here, like the scripts for interacting with users
class ClientModel:
    
    CHAT_LOG_FILE = "chat_log.txt"
    TIMEOUT_VAL = 2 #seconds
    
    def __init__(self):
	pass
	
    def get_poll_timeout(self):
	return self.TIMEOUT_VAL
        
    def save_chat_log(self, chat_log):
        log_file = open(self.CHAT_LOG_FILE, 'w')
        log_file.write(chat_log)
        log_file.close()
    

#view handles all communication with console (the view for our application, what people interact with)
class ClientView:
    
    display_text = ""
    
    def get_user_input(self, message = ""):
	
	if ( message == "" ):
	    #get user input, blocking call (strip whitespace for sending messages)
	    return sys.stdin.readline().rstrip()
	else:
	    return raw_input(message)
	
    def display(self, data):
	self.display_text += data + "\n"
	print(data)
	
    def add_to_chat_script(self, data):
	self.display_text += data + "\n"
	
    def get_display_text(self):
	return self.display_text
    
    
#controller inherits from Handler (handler controls interactions so its logical to use this as control for MVC)
class ClientControl(Handler):
    
    model = None
    view = None
    
    havePingResponse = False
    endTime = 0
    
    def on_close(self):
	self.view.display("Goodbye!")
	sys.exit() #doesnt work well, since this is in a child thread, it doesnt kill main python process
    
    def on_msg(self, msg):

	#do not print ping response, just record when message back is received and set flag
	if ( 'data' in msg ):
	    
	    if ( msg['data'].lower() == "ping" ):
		self.havePingResponse = True #use owner to access outer class
		self.endTime = time.time() * 1000
	elif ( 'join' in msg ):
	    self.view.display("{} has joined the chat!".format(msg['join']))
		
	elif ( 'speak' in msg ): #possibly have view handle how to display data....
	    view.display("{}: {}".format(msg['speak'], msg['txt']))
	    
	else:
	    pass #ignore possible invalid messages
	
    #no need for self since this will only be called internally
    def periodic_poll(self):
	while 1:
	    poll()
	    sleep(0.05)  # seconds

    def start_control(self, model, view):

	self.model = model
	self.view = view
	
	TIMEOUT_VAL = model.get_poll_timeout() #get timeout value from model
	
	myname = view.get_user_input('What is your name? ')
	self.view.add_to_chat_script('What is your name? ')
	self.do_send({'join': myname})
	
	thread = Thread(target=self.periodic_poll)
	thread.daemon = True  # die when the main thread dies 
	thread.start()

	while 1:
	    
	    mytxt = view.get_user_input()
	    self.view.add_to_chat_script(mytxt) #add what user is typing to chat script

	    #save chat script to file (retreive from view, use model to store)
	    if ( mytxt.lower() == "s" ):
		
		self.model.save_chat_log(self.view.get_display_text())
		self.view.display("Chat Log Saved")
		
	    elif ( mytxt.lower() == "q" ):
		
		self.do_close()
		
	    elif ( mytxt.lower() == "e" ):
		self.view.display("FUN EASTER EGG HERE...")
		#fun easter egg goes here...
	    
	    #send ping to server to see if its still up
	    elif ( mytxt.lower() == "ping" ):
		
		self.view.display("Pinging chat server, sending {} bytes.".format(sys.getsizeof("ping")));
		self.do_send({'data':mytxt}) #data key when sending data to server
            
		#time ping interaction			
		startTime = time.time() * 1000   #milliseconds

		#wait for response (use global but don't need keyword in since we aren't re-defining)
		poll_for(TIMEOUT_VAL) # in seconds
        
		#check if the flag has been ticked (got ping response back)
		if ( (not self.havePingResponse) ):
		    self.view.display("No response from server, timed out after {:.2} seconds.".format(time.time() - (startTime/1000)))
		else:
		    view.display("Server responded after {} ms\n".format((self.endTime - startTime)))
		    self.havePingResponse = False #reset
            
	    else: #if no special messages are found just default to sending chat type message
		self.do_send({'speak':myname, 'txt':mytxt}) #default interaction, just name with text	
		
		
		
if __name__ == "__main__" :
    
    model = ClientModel()
    view = ClientView()
    control = ClientControl('localhost', 8888)
    
    control.start_control(model, view)
		
		
		
