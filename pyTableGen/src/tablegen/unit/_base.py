import logging

class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __instancecheck__(cls, instance, /) -> bool:
        logging.debug('call instance check @ MetaTableGenType.__instancecheck__', cls.__name__, instance)
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)

class TableGenType(metaclass=MetaTableGenType):
    
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

    def __defname__(self)->str:
        try:
            return self.__name
        except AttributeError:
            return self.__class__.__name__.lower()

    @property
    def defname(self):
        return self.__defname__()

class RecordType(TableGenType):

    def check(cls, instance):
        pass

class Unset:
    pass

