import logging

class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)
        cls.named_values = dict()

    def __instancecheck__(cls, instance, /) -> bool:
        logging.debug('call instance check @ MetaTableGenType.__instancecheck__', cls.__name__, instance)
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)
    
    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        
        if hasattr(instance, "__late_init__") and callable(instance.__late_init__):
            instance.__late_init__()

        instance.__reset_field__ = set()
        
        return instance

    def __setattr__(self, name: str, value, /) -> None:
        '''
        Bind the name of the object to the object itself, and check the type of the value
        It's a sugar for the user to bind the object to the name, semantic is no different
        '''
        if isinstance(type(value), MetaTableGenType):
            if not isinstance(value, self):
                logging.warning(f"Assign {self.__name__}.{name} with {type(value).__name__} value is unexpect")
            if not value.hasName():
                value.bind(name, self)
        return super().__setattr__(name, value)

class _TableGenType:
    '''
    Magic methods for TableGenType for override
    '''
    def __iscomplex__(self)->bool:
        return False

    def __type__(self):
        return self.__class__

    @classmethod
    def __class_dump__(cls):
        return cls.__name__

    def __dump__(self):
        return f"<Record of {type(self).__class_dump__()}>"

class TableGenType(_TableGenType, metaclass=MetaTableGenType):
    _hasName = False
    __recname__: str
    
    def bind(self, name:str, parent=None):
        self.__recname__ = name
        self.__parent = parent
        self._hasName = True
        return self

    @property
    def parent(self):
        try:
            return self.__parent
        except AttributeError:
            return None
    
    def isComplex(self):
        return self.__iscomplex__()

    def hasName(self):
        return self._hasName

    def getType(self):
        '''
        Get the type of the object, tablegen type has complex subtypes
        e.g. bits<3> is a subtype of bits, but python cannot get it with type()
        because of python is dynamic language and ducky typing, which is meaningless
        getType only use to "Dumper", to get exact type of the object for tablegen
        '''
        return self.__type__()

    @property
    def defname(self):
        try:
            return self.__recname__ # type: ignore
        except AttributeError:
            return self.__class__.__name__.lower()

class Unset(TableGenType):
    __instance = dict()
    
    def __new__(cls, t):
        try:
            return cls.__instance[t]
        except KeyError:
            cls.__instance[t] = super().__new__(cls)
            return cls.__instance[t]
    
    def __init__(self, type):
        self.__type = type

    def __type__(self): # type: ignore
        return self.__type
    
    def __defname__(self):
        return 'unset'

    def __repr__(self) -> str:
        return '??'

