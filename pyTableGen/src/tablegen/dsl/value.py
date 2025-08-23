class Unset:
    ''' it is used to represent unset value `?` in TableGen'''
    __instance = dict()

    def __new__(cls, t):
        try:
            return cls.__instance[t]
        except KeyError:
            cls.__instance[t] = super().__new__(cls)
            return cls.__instance[t]
    
    def __init__(self, type):
        self._type = type

class Unknown:
    ''' 
    This is a dummy value for TableGen, it is used to represent unknown value
    If we use "TableGenClass" to define a Record,
    because we not sure the 'definition' inside TableGen
    we will place a UnknownValue to represent it.
    '''
    __instance = dict()

    def __new__(cls, t):
        try:
            return cls.__instance[t]
        except KeyError:
            cls.__instance[t] = super().__new__(cls)
            return cls.__instance[t]
    
    def __init__(self, type):
        self._type = type