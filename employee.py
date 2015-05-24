from client import *

#create new view just for employees
class EmployeeView:
    
    #will be updating later
    
    def __init__(self):
        pass


if __name__ == "__main__" :
    
    model = ClientModel()
    view = EmployeeView()
    control = ClientControl('localhost', 8888)
    
    control.start_control(model, view)
