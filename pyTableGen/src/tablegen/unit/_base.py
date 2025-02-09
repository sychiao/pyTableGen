import logging

class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __instancecheck__(cls, instance, /) -> bool:
        logging.debug('call instance check @ MetaTableGenType.__instancecheck__', cls.__name__, instance)
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)

class _TableGenType:
    '''
    Magic methods for TableGenType for override
    '''

    def __defname__(self)->str:
        try:
            return self.__name # type: ignore
        except AttributeError:
            return self.__class__.__name__.lower()

class TableGenType(_TableGenType, metaclass=MetaTableGenType):
    
    def bind(self, name:str, ctx=None):
        self.__name = name
        self.__ctx = ctx
        return self

    @property
    def Ctx(self):
        try:
            return self.__ctx
        except AttributeError:
            return None

    @property
    def defname(self):
        return self.__defname__()

class Unset(TableGenType):
    
    def __defname__(self):
        return 'unset'

