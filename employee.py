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
        self.displayData = ""
        
        if ( isinstance(data, basestring) ):
            self.displayData = data
        elif ( 'join' in data ):
            self.displayData = "\n{} has joined the chat!\n".format(data['join'])
            
            issue = ""
            if ( data['support'] == "1" ) :
                issue = "Complaints"
            elif ( data['support'] == "2" ) :
                issue = "Questions"
            elif ( data['support'] == "3" ) :
                issue = "Installation Support"
            elif ( data['support'] == "4" ) :
                issue = "Find my order"
                
            self.displayData += "{} selected '{}' for this chat\n".format(data['join'], issue)
            self.displayData += "Summary of {}'s problems: \n".format(data['join']) + data['summary'] + "\n"
        
        elif ( 'speak' in data ):
            self.displayData = "{}: {}".format(data['speak'], data['txt'])
            
        elif ( 'leave' in data ):
            self.displayData = "{} has logged off.".format(data['leave'])
        else:
            return #dont display things that you dont understand
        
        self.display_text += self.displayData + "\n"
        print(self.displayData)
	
    def add_to_chat_script(self, data):
        self.display_text += data + "\n"
	
    def get_display_text(self):
        return self.display_text


if __name__ == "__main__" :
    
    model = ClientModel()
    view = EmployeeView()
    control = ClientControl('localhost', 8888)
    
    control.start_control(model, view)
