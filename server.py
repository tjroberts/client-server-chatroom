from network import Listener, Handler, poll

 
handlers = {}  # map client handler to user name
 
class MyHandler(Handler):
    
    def on_open(self):
        pass
        
    def on_close(self):
        pass
     
    def on_msg(self, msg):
        
        #server figures out what to do depending on keys in dict
        if ( 'join' in msg ):
            print("{} has joined the chat!".format(msg['join']))
        elif ( 'data' in msg ): #server has been sent just data
            
            if ( msg['data'].lower() == "ping" ):
                print("got ping")
                self.do_send("ping") #just send ping back
            
        elif ('speak' in msg ):
            print("{}: {}".format(msg['speak'], msg['txt'])); # just print what they are saying
        else:
            pass



port = 8888
server = Listener(port, MyHandler)
while 1:
    poll(timeout=0.05) # in seconds


