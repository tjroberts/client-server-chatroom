from network import Listener, Handler, poll

#could delcare all relevant data here, like the scripts for interacting with users
class ServerModel:
    
    def __init__(self):
        pass

class ServerView:
    
    @staticmethod     #decorator for declaring static methods
    def display(data):
        print(data)

 
#MyHandler inherits from Handler, we do this so we can pass it to the Listener below
#this is similar to controller
class ServerControl(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        
        #server figures out what to do depending on keys in dict
        if ( 'join' in msg ):
            ServerView.display("{} has joined the chat!".format(msg['join']))
        elif ( 'data' in msg ): #server has been sent just data
            
            if ( msg['data'].lower() == "ping" ): #if the contents of data msg are ping
                ServerView.display("got ping")
                self.do_send("ping") #just send ping back
            
        elif ('speak' in msg ): #if chat message
            ServerView.display("{}: {}".format(msg['speak'], msg['txt'])); # just print what they are saying
        else:
            pass

if __name__ == "__main__" :

    handlers = {}  # map client handler to user name

    port = 8888
    server = Listener(port, ServerControl)
    while 1:
        poll(timeout=0.05) # in seconds

    
