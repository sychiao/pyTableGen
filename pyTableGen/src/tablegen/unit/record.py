from ..binding import IntInit, StringInit, ListInit, DefInit
import tablegen.binding as binding
import weakref
from typing import ClassVar, Any
import typing

from ._base import LazyProperty, TableGenType, LazyAttr
from .bits import Bits
from .dag import DAG

def Init2Value(v: binding.Init , ctx=None):
    if isinstance(v, binding.IntInit):
        return v.getValue() # int
    elif isinstance(v, binding.BitInit):
        return v.getValue() # bool
    elif isinstance(v, binding.BitsInit):
        numbits = v.getNumBits()
        bitsstr = "".join([v.getBit(idx).getAsString() for idx in range(numbits)])
        return Bits(bitsstr)
    elif isinstance(v, binding.StringInit):
        return v.getAsString()
    elif isinstance(v, binding.ListInit):
        return [Init2Value(e, ctx) for e in v.getValues()]
    elif isinstance(v, binding.DefInit):
        return TableGenRecordWrapper(v.getDef())
    elif isinstance(v, binding.DagInit):
        return "DAG"
    else:
        return f"Unknonw {v.getAsString()}"

class TableGenContext:

    def __init__(self):
        self.records = dict()

    def addRecord(self, recobj):
        self.records[recobj.recname] = recobj
    
    def getRecord(self, name):
        return self.records.get(name)

class TableGenRecord(TableGenType):

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
        self._ctx = ctx

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

    def __getattr__(self, key: str):
        Value = Init2Value(self._rec.getValue(key).getValue(), self._ctx)
        self.__dict__[key] = Value
        return Value

    def __late_init__(self):
        for key in self.fields:
            if key not in self.__dict__:
                self.__dict__[key] = Init2Value(self._rec.getValue(key).getValue(), self._ctx)

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
