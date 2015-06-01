from client import *

#create new view just for employees
class EmployeeView:
    
    display_text = ""
    employeeData = {}
    
    def display_initial_dialogue(self):
        self.employeeData['join'] = self.get_user_input("Hello GTAModders employee, please enter your name: ")
	
    def get_dialogue_data(self):
        return self.employeeData;
    
    def get_user_input(self, message = ""):

        if ( message == "" ):
            #get user input, blocking call (strip whitespace for sending messages)
            return sys.stdin.readline().rstrip()
        else:
            return raw_input(message)
	
    def display(self, data):
        displayData = ""
        
        if ( activate_easter_egg ) :
            displayData += '\033[1;36m' #make colored text for easter egg (can cause problems in IDLE or terminals that don't support color)
        else:
            displayData += '\033[0m'
        
        if ( isinstance(data, basestring) ):
            displayData += data
        elif ( 'join' in data ):
            displayData += "\n{0} has joined the chat!\n".format(data['join'])
            
            issue = ""
            if ( data['support'] == "1" ) :
                issue = "Complaints"
            elif ( data['support'] == "2" ) :
                issue = "Questions"
            elif ( data['support'] == "3" ) :
                issue = "Installation Support"
            elif ( data['support'] == "4" ) :
                issue = "Find my order"
                
            displayData += "{0} selected '{1}' for this chat\n".format(data['join'], issue)
            displayData += "Summary of {0}'s problems: \n".format(data['join']) + data['summary'] + "\n"
        
        elif ( 'speak' in data ):
            displayData += "{0}: {1}".format(data['speak'], data['txt'])
            
        elif ( 'leave' in data ):
            displayData += "{0} has logged off.".format(data['leave'])
        else:
            return #dont display things that you dont understand
        
        self.display_text += displayData + "\n"
        print(displayData)
	
    def add_to_chat_script(self, data):
        self.display_text += data + "\n"
	
    def get_display_text(self):
        return self.display_text


if __name__ == "__main__" :
    
    response = raw_input("Please specify an IP address (enter to use local IP): ")
    
    if ( response == "" ):
        IP = get_my_ip()
    else :
        IP = response
    
    model = ClientModel()
    view = EmployeeView()  #pass it employee view
    control = ClientControl(IP, 12345)
    
    control.start_control(model, view)
