class Record:

    def __init__(self, name):
        self.__name__ = name
    
    def __name__(self):
        pass

    def isClass(self):
        pass

a = Record("name")
print(a.__name__)