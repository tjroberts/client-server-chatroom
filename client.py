from network import Handler, poll, poll_for, get_my_ip
import sys
from threading import Thread
from time import sleep
import re

import time

activate_easter_egg = False

#could delcare all relevant data here, like the scripts for interacting with users
class ClientModel:
    
    CHAT_LOG_FILE = "chat_log.txt"
    TIMEOUT_VAL = 2 #seconds
    
    def __init__(self):
	pass
	
    def get_poll_timeout(self):
	return self.TIMEOUT_VAL
        
    def save_chat_log(self, chat_log):
	chat_log = re.sub(r'\033\[1;36m', '', chat_log) #remove ANSI color strings
	chat_log = re.sub(r'\033\[0m', '', chat_log) #remove ANSI color strings
        log_file = open(self.CHAT_LOG_FILE, 'w')
        log_file.write(chat_log)
        log_file.close()
    

class CustomerView:
    
    display_text = ""
    clientData = {}
    supportType = {"1": "Complaints", "2": "Questions", "3": "Installation Support", "4": "Find my order"}
    
    def display_initial_dialogue(self):
	self.clientData['join'] = self.get_user_input("Welcome to GTAModders customer support \nWhat is your name: ")
	self.clientData['support'] = self.get_user_input("Hello {0}, what type of support do you need(1. Complaints, 2. Questions, 3. Installation Support, 4. Find my order): ".format(self.clientData['join']))
	self.clientData['summary'] = self.get_user_input("Welcome to {0}, please enter a summary of your issue: \n".format(self.supportType[self.clientData['support']]))
	
    def get_dialogue_data(self):
	return self.clientData
    
    def get_user_input(self, message = ""):
	
	if ( message == "" ):
	    return sys.stdin.readline().rstrip()
	else:
	    return raw_input(message)
	
    def display(self, data):
	
	displayData = ""
	
        if ( activate_easter_egg ) :
            displayData += '\033[1;36m' #make colored text for easter egg
        else:
            displayData += '\033[0m'
	
	if ( isinstance(data, basestring) ): #this wont work in python 3.X only compatible with 2.X (change basestring to str)
	    displayData += data
	elif ( 'join' in data ):
	    displayData += "Hello my name is {0}, I am pleased to assist you.".format(data['join'])
	elif ( 'speak' in data ):
	    displayData += "{0}: {1}".format(data['speak'], data['txt'])
        elif ( 'leave' in data ):
            displayData += "{0} has logged off.".format(data['leave'])
	else:
	    return #dont display things you dont understand
	
	print(displayData)
	self.display_text += displayData + "\n"
	
    def add_to_chat_script(self, data):
	self.display_text += data + "\n"
	
    def get_display_text(self):
	return self.display_text
    
    
class ClientControl(Handler):
    
    model = None
    view = None
    dialogueData = None
    still_connected = True
    
    havePingResponse = False
    endTime = 0
    
    def on_close(self):
	self.view.display("Goodbye!")
	self.still_connected = False
	sys.exit()                     #kill polling thread
    
    def on_msg(self, msg):

	if ( 'data' in msg ):
	    if ( msg['data'].lower() == "ping" ):
		self.havePingResponse = True #use owner to access outer class
		self.endTime = time.time() * 1000
	else:
	    self.view.display(msg)
	
    def periodic_poll(self):
	while 1:
	    poll()
	    sleep(0.05)  # seconds

    def start_control(self, model, view):

	global activate_easter_egg
	self.model = model
	self.view = view
	
	TIMEOUT_VAL = model.get_poll_timeout() 
	
	#interaction here varies depending on view (employee/customer)
	self.view.display_initial_dialogue()
	self.dialogueData = self.view.get_dialogue_data()
	self.do_send(self.dialogueData) #send initial data, depends on which view it being used
	
	thread = Thread(target=self.periodic_poll)
	thread.daemon = True  # die when the main thread dies 
	thread.start()

	while self.still_connected:
	    
	    mytxt = view.get_user_input()
	    self.view.add_to_chat_script(mytxt) #add what user is typing to chat script

	    if ( mytxt.lower() == "s" ):
		self.model.save_chat_log(self.view.get_display_text())
		self.view.display("Chat Log Saved")
		
	    elif ( mytxt.lower() == "q" ):
		self.do_close()
		
	    elif ( mytxt.lower() == "e" ):
		if ( activate_easter_egg ):
		    activate_easter_egg = False
		else:
		    activate_easter_egg = True
	    
	    elif ( mytxt.lower() == "ping" ):
		
		self.view.display("Pinging chat server, sending {0} bytes.".format(sys.getsizeof("ping")));
		self.do_send({'data':mytxt}) #data key when sending data to server
            			
		startTime = time.time() * 1000   #milliseconds
		poll_for(TIMEOUT_VAL) # in seconds
        
		if ( (not self.havePingResponse) ):
		    self.view.display("No response from server, timed out after {0:.2} seconds.".format(time.time() - (startTime/1000)))
		else:
		    view.display("Server responded after {0:.4} ms\n".format((self.endTime - startTime)))
		    self.havePingResponse = False #reset
	    else: 
		self.do_send({'speak':self.dialogueData['join'], 'txt':mytxt}) #default interaction, just name with text	
		
		
if __name__ == "__main__" :
    
    #IP = '192.168.1.89'
    IP = get_my_ip() #change when this is running on different computer
    
    model = ClientModel()
    view = CustomerView() #pass it the customer view
    control = ClientControl(IP, 12345)
    
    control.start_control(model, view)
		
		
		
