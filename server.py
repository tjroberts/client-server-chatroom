from network import Listener, Handler, poll

#part of model, had to be global though :(
handlers = {}

#could delcare all relevant data here, like the scripts for interacting with users
class ServerModel:
    
    all_users = {} #empty dictionary
    
    def __init__(self):
        pass
    
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
        self.distribute_message({'leave': "{}".format(self.model.get_all_users()[self])})
        self.model.remove_user(self)
        
    #distribute message from user to all other users
    def distribute_message(self, message):
        
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
            self.view.display("{} has joined the chat!".format(msg['join'])) #print on server for debug
            self.model.add_user(msg['join'], self)

            if ( len(self.model.get_all_users()) > 2 ) :
                self.do_send({'speak':'GTAModders Support', 'txt':'Sorry all customer support representatives are busy, please try again later.'})
                self.do_close() #terminate the connection
            else:
                self.distribute_message(msg)
            
        elif ( 'data' in msg ):
            
            if ( msg['data'].lower() == "ping" ):
                self.do_send({"data":"ping"}) #just send ping back
            
        elif ('speak' in msg ): 
            self.view.display("{}: {}".format(msg['speak'], msg['txt'])); # just print what they are saying
            self.distribute_message(msg)

if __name__ == "__main__" :

    port = 8888
    server = Listener(port, ServerControl)
    
    while 1:
        poll(timeout=0.05) # in seconds

    
