from network import Listener, Handler, poll, poll_for, get_my_ip

#part of model, had to be global though :(
handlers = {}

#could delcare all relevant data here, like the scripts for interacting with users
class ServerModel:
    
    all_users = {} #empty dictionary
    waiting_users = []
    
    def __init__(self):
        pass
    
    #WAIT USERS
    def add_wait_user(self, username, handler, message):
        self.waiting_users.append((handler, username, message)) #tuple
        
    def remove_wait_user(self, user):
        self.waiting_users.remove(user)
        
    def get_wait_users(self):
        return self.waiting_users
    
    #ALL USERS
    def add_user(self, username, handler):
        self.all_users[handler] = username
        
    def remove_user(self, handler):
        del self.all_users[handler]
        
    def get_all_users(self):
        return self.all_users
        

class ServerView:
    
    def __init__(self):
        pass
    
    def display(self, data):
        print(data)


class ServerControl(Handler):
    
    model = ServerModel()
    view = ServerView()
    
    def on_open(self):
        pass
        
    def on_close(self):
        #send leave message with name of user that logged off
        self.distribute_message({'leave': "{0}".format(self.model.get_all_users()[self])}) 
        self.model.remove_user(self)
        
        #let next user in
        if ( len(self.model.get_wait_users()) > 0 ):
            first_in_line = self.model.get_wait_users()[0] 
            self.model.add_user(first_in_line[1], first_in_line[0])
            self.model.remove_wait_user(first_in_line)
            first_in_line[0].do_send({'speak':'GTAModders Support', 'txt':'You are now being connected to a customer service representative'})
            first_in_line[0].distribute_message(first_in_line[2])
        
    #distribute message from user to all other users
    def distribute_message(self, message):
        
        if ( self in self.model.get_all_users() ): #only distribute to people who have joined all_users
        
            all_users = self.model.get_all_users()
            if ( 'join' in message ):
                
                for userHandle in all_users:
                    if ( not all_users[userHandle] == message['join'] ): #dont send to the guy who joined
                        userHandle.do_send(message)
                        
            elif ( 'speak' in message ):
                for userHandle in all_users:
                    if ( not all_users[userHandle] == message['speak'] ): #dont send to the guy that wrote the message
                        userHandle.do_send(message)
                        
            elif ( 'leave' in message ):
                for userHandle in all_users:
                    if ( not all_users[userHandle] == message['leave'] ):
                        userHandle.do_send(message)
            
     
    def on_msg(self, msg):
        
        if ( 'join' in msg ):
            #self.view.display("{} has joined the chat!".format(msg['join'])) #print on server for debug
            
            if ( 'support' in msg ) : #for clients
                
                if ( len(self.model.get_all_users()) == 2 ) :
                    self.model.add_wait_user(msg['join'], self, msg)
                    self.do_send({'speak':'GTAModders Support', 'txt':'Sorry all customer service agents are busy, please wait.'})
                else:
                    self.model.add_user(msg['join'], self)
                    self.do_send({'speak':'GTAModders Support', 'txt':'You are now being connected to a customer service representative'})
                    self.distribute_message(msg)
                
            else: #for employees
                self.model.add_user(msg['join'], self)
                self.distribute_message(msg)
            
        elif ( 'data' in msg ):
            
            if ( msg['data'].lower() == "ping" ):
                self.do_send({"data":"ping"}) #just send ping back
            
        elif ('speak' in msg ): 
            #self.view.display("{0}: {1}".format(msg['speak'], msg['txt'])); # just print what they are saying #display chat for debug
            self.distribute_message(msg)

if __name__ == "__main__" :

    port = 12345
    
    print(get_my_ip())
    
    server = Listener(port, ServerControl)
    while 1:
        poll(timeout=0.05) # in seconds

    
