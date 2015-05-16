Hello fellow group members!

General Explanations:

We don't really have to do much with the actual network communication, its all handle by the json architecture and the asyncore module.
Not sure we are going to really need to add any other poll() calls or anything but keep in mind that all communication is asynchronous 
and when you call poll() the code continues on and the "on_msg()" method acts as a callback and is called by another thread that is
polling for input on the socket after you call poll(). You can look at json and asyncore if your curious how it is working at the socket level.

The way I organized it so far (may change since nothing is in classes or organized well) is that each message to the server is a python dictionary. 
The dictionary only has one entry and the key determines the type of message. You can use the python expression var1 in dict1. This will return 
True if var1 is a key in dict1. So this is how I determine the type of message the client is sending. So I did data for things like "ping" and possibly
any other system type processes sent to the server. If the key speak is found, it just prints out chat information.

The way I did the timeout when waiting for the ping (just in case server is offline) is with a global variable for the end time as well as a flag.
The poll_for() function will let you poll and wait in the poll call for the specified amount of seconds. If the callback function on_msg() did not
receive a ping message back the flag will never be set to true. So thats how I determine if there is a response. A negative side effect is that
when it receives the response it will still wait for the specified time in poll_for(). Still, the endTime variable will be correct because the callback
on_msg() is called immediately upon receipt of a message.

Most of the work we are going to have to do is just in the class methods defined in the server and client. We may have to add new
types of keys or just some more selection statements. And try to rearrage everything to follow MVC structure. (maybe divide into more classes?)
The method names all refer to events that happen on that files (client/server) side of the socket. 

Hopefully this wasn't to long winded, let me know if anyone has questions. 