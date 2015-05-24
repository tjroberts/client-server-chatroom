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
        
    def get_all_users(self):
        return self.all_users
        

class ServerView:
    
    def __init__(self):
        pass
    
    def display(self, data):
        print(data)

 
#MyHandler inherits from Handler, we do this so we can pass it to the Listener below
#this is similar to controller

class ServerControl(Handler):
    
    model = ServerModel()
    view = ServerView()
    
    def on_open(self):
        pass
        
    def on_close(self):
        pass
        
    #distribute message from user to all other users
    def distribute_message(self, message):
        
        #get dictionary of all user handles (keys) and usernames (values)
        all_users = self.model.get_all_users()
        
        #join message has different structure and needs to be handled seperately (rather than 'speak' types handles in else)
        if ( 'join' in message ):
            
            for userHandle in all_users:
                if ( not all_users[userHandle] == message['join'] ): #dont send to the guy who joined
                    userHandle.do_send(message)
        else:
            for userHandle in all_users:
                if ( not all_users[userHandle] == message['speak'] ): #dont send to the guy that wrote the message
                    userHandle.do_send(message)
     
    def on_msg(self, msg):
        
        #server figures out what to do depending on keys in dict
        if ( 'join' in msg ):
            self.view.display("{} has joined the chat!".format(msg['join'])) #print on server for debug
            self.distribute_message(msg)
            self.model.add_user(msg['join'], self)
            
        elif ( 'data' in msg ): #server has been sent just data
            
            if ( msg['data'].lower() == "ping" ): #if the contents of data msg are ping
                #self.view.display("got ping") #for debug
                self.do_send({"data":"ping"}) #just send ping back
            
        elif ('speak' in msg ): #if chat message
            self.view.display("{}: {}".format(msg['speak'], msg['txt'])); # just print what they are saying
            
            #send to all other users except sending user
            self.distribute_message(msg)
        else:
            pass

if __name__ == "__main__" :

    port = 8888
    server = Listener(port, ServerControl)
    
    while 1:
        poll(timeout=0.05) # in seconds

    
