from ..binding import IntInit, StringInit, ListInit, DefInit
import tablegen.binding as binding
import weakref
from typing import ClassVar, Any, Protocol
import typing

from ._base import LazyProperty, TableGenType, LazyAttr
from .bits import Bits
from .dag import DAG

class ContextProtocol(Protocol):
    def getValuefromInit(self, v: binding.Init):
        ...

class EmptyContext:
    def getValuefromInit(self, v: binding.Init):
        return None

class TableGenRecord(TableGenType):

    def setCtx(self, ctx):
        self._ctx = ctx

    @property
    def Ctx(self):
        if self._ctx:
            return self._ctx
        else:
            self._ctx = EmptyContext()
            return self._ctx

    def __recname__(self)->str:
        raise NotImplementedError

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

class TableGenRecordWrapper(TableGenRecord):
    __cached__ = weakref.WeakValueDictionary()

    def __init_subclass__(cls):
        cls.__cached__ = weakref.WeakValueDictionary()

    def __new__(cls, obj, ctx=None):
        if cached := cls.__cached__.get(id(obj)):
            return cached
        if issubclass(obj.__class__, TableGenRecord):
            return obj
        ins = super().__new__(cls)
        cls.__cached__[id(obj)] = ins
        return ins

    def __init__(self, rec: binding.Record, ctx=None):
        self._rec = rec
        self.setCtx(ctx)

    @LazyAttr
    def __recname__(self):
        return self._rec.getName()

    @LazyAttr
    def __classes__(self):
        return tuple(record.getName() for record, _ in self._rec.getSuperClasses())

    @LazyAttr
    def __base__(self):
        return tuple(record.getName() for record in self._rec.getType().getClasses())
    
    @LazyAttr
    def __fields__(self):
        return {RecVal.getName() for RecVal in self._rec.getValues()}

    @LazyAttr
    def __item__(self):
        self.__late_init__()
        return {key: self.__dict__[key] for key in self.fields}

    def _getValueInit(self, key: str):
        return self._rec.getValue(key).getValue()

    def _getValue(self, key: str):
        return self.Ctx.getValuefromInit(self._getValueInit(key))

    def __getattr__(self, key: str):
        self.__dict__[key] = self._getValue(key)
        return self.__dict__[key]

    def __late_init__(self):
        for key in self.fields:
            if key not in self.__dict__:
                self.__dict__[key] = self._getValue(key)

    def cast(self, cls):
        if isinstance(self, cls):
            return cls.wrap(self._rec)
        return None

    def safe_cast(self, cls) -> 'TableGenRecord':
        if isinstance(self, cls):
            return cls.wrap(self._rec)
        return self

class TypedRecord(TableGenRecord):

    def __init_subclass__(cls) -> None:
        cls.__wrapped__ = type(f'{cls.__name__}Wrapper', (TableGenRecordWrapper, cls), {})

    @LazyAttr
    def __fields__(self):
        return {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}

    def __classes__(self) -> tuple[str, ...]:
        return tuple(cls.__name__ for cls in type(self).__mro__ if issubclass(cls, TypedRecord))

    def __base__(self) -> tuple[str, ...]:
        return (type(self).__name__, )

    def __item__(self) -> dict[str, Any]:
        return {key: self.__dict__[key] for key in self.fields}
    
    @classmethod
    def wrap(cls, rec):
        return cls.__wrapped__(rec)
