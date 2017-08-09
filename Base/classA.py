class student():
    def __init__(self,name,score):
        self.__name=name
        self.__score=score
        
    def show(self):
        print("name:",self.__name,";score:",self.__score)
        
class wang(student):
    pass