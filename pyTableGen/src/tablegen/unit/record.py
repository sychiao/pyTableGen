# from ..binding import IntInit, StringInit, ListInit, DefInit
# import tablegen.binding as binding
# import weakref
from typing import ClassVar, Any
import typing

from ._base import TableGenType
#from .bits import Bits
#from .dag import DAG
from ..utils import LazyAttr

class TableGenRecord(TableGenType):

    def setCtx(self, ctx):
        self._ctx = ctx

    @property
    def Ctx(self):
        try:
            return self._ctx
        except AttributeError:
            return None

    def bind(self, name:str):
        self.__name = name
        return self

    def __recname__(self)->str:
        try:
            return self.__name
        except AttributeError:
            return self.__class__.__name__.lower()

    def __fields__(self)->set[str]:
        raise NotImplementedError

    def __base__(self)->tuple[str, ...]:
        raise NotImplementedError
    
    def __classes__(self)->tuple[str, ...]:
        raise NotImplementedError

    def __item__(self)->dict[str, Any]:
        raise NotImplementedError

    @property
    def recname(self):
        return self.__recname__()

    @property
    def fields(self):
        return self.__fields__()
    
    @property
    def bases(self):
        return self.__base__()
    
    @property
    def classes(self):
        return self.__classes__()

    @property
    def items(self):
        return self.__item__()

    @classmethod
    def check(cls, ins):
        return cls.__name__ in ins.classes

    def __repr__(self):
        return f"<{self.recname}: {self.bases} {self.items}>"

    def safe_cast(self, cls):
        return self

class TypedRecord(TableGenRecord):

    #def __init_subclass__(cls) -> None:
    #    cls.__wrapped__ = type(f'{cls.__name__}Wrapper', (TableGenRecordWrapper, cls), {})

    @LazyAttr
    def __fields__(self):
        return {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}

    def __classes__(self) -> tuple[str, ...]:
        return tuple(cls.__name__ for cls in type(self).__mro__ if issubclass(cls, TypedRecord))

    def __base__(self) -> tuple[str, ...]:
        return (type(self).__name__, )

    def __item__(self) -> dict[str, Any]:
        return {key: self.__dict__[key] for key in self.fields}
    
    #@classmethod
    #def wrap(cls, rec):
    #    return cls.__wrapped__(rec)
