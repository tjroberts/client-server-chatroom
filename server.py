from network import Listener, Handler, poll

#could delcare all relevant data here, like the scripts for interacting with users
class ServerModel:
    
    all_users = {} #empty dictionary
    
    def __init__(self):
        pass
    
    def add_user(self, username, handler):
        self.all_users[handler] = username
        
    def get_all_users(self):
        return self.all_users
        
    def save_chat_script(self):
        #save to predefined file
        pass
    

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
        
        #get handle for user
        all_users = self.model.get_all_users()
        
        for userHandle in all_users:
            if ( not all_users[userHandle] == message['speak'] ): #dont send to the guy that wrote the message
                userHandle.do_send({'speak':message['speak'], 'txt':message['txt']})
     
    def on_msg(self, msg):
        
        #server figures out what to do depending on keys in dict
        if ( 'join' in msg ):
            self.view.display("{} has joined the chat!".format(msg['join']))
            self.model.add_user(msg['join'], self)
            
        elif ( 'data' in msg ): #server has been sent just data
            
            if ( msg['data'].lower() == "ping" ): #if the contents of data msg are ping
                self.view.display("got ping")
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

    
