class Unset:
    ''' it is used to represent unset value `?` in TableGen'''
    pass

class Unknown:
    ''' 
    This is a dummy value for TableGen, it is used to represent unknown value
    If we use "TableGenClass" to define a Record,
    because we not sure the 'definition' inside TableGen
    we will place a UnknownValue to represent it.
    '''
    pass