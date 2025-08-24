class PlaceholdType:
    ''' This is a dummy type for TableGen, it is used to represent unknown type
    If we use "TableGenClass" to define a Record,
    because we not sure the 'definition' inside TableGen
    we will place a PlaceholdType to represent it.
    '''
    _instance = dict()

    def __new__(cls, t):
        try:
            if isinstance(t, type):
                return cls._instance[t.__name__]
            else:
                return cls._instance[type(t).__name__]
        except KeyError:
            if isinstance(t, type):
                cls._instance[t.__name__] = super().__new__(cls)
                return cls._instance[t.__name__]
            else:
                cls._instance[type(t).__name__] = super().__new__(cls)
                return cls._instance[type(t).__name__]
    
    def __init__(self, t):
        self.__type = t

    def getType(self):
        return self.__type

class Unset(PlaceholdType):
    ''' it is used to represent unset value `?` in TableGen'''
    _instance = dict()

    def __str__(self):
        return f"?"
    
    def __repr__(self):
        return f'Unset({repr(self.getType())})'

class UnknownValue(PlaceholdType):
    ''' 
    This is a dummy value for TableGen, it is used to represent unknown value
    If we use "TableGenClass" to define a Record,
    because we not sure the 'definition' inside TableGen
    we will place a UnknownValue to represent it.
    '''
    _instance = dict()

    def __str__(self):
        return "Unk"
    
    def __repr__(self):
        return f'UnknownValue({repr(self.getType())})'