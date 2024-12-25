from ..binding import IntInit, StringInit, ListInit, DefInit
import tablegen.binding as binding
import weakref
from typing import ClassVar
import typing

from ._base import LazyProperty, TableGenType
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
        return TableGenRecord(v.getDef())
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


import time

class TableGenRecord(TableGenType):
    __cached__: ClassVar[weakref.WeakValueDictionary] = weakref.WeakValueDictionary()

    def __init_subclass__(cls):
        cls.__cached__ = weakref.WeakValueDictionary()

    def __new__(cls, obj, ctx=None):
        #s = time.time()
        #if ctx and (ins := ctx.getRecord(obj.getName())):
        #    return ins
        if cached := cls.__cached__.get(id(obj)):
            return cached
        if issubclass(obj.__class__, TableGenRecord):
            return obj
        ins = super().__new__(cls)
        cls.__cached__[id(obj)] = ins
        #e = time.time()
        #print("rev", e - s)
        return ins

    def __init__(self, rec: binding.Record, ctx=None):
        self._rec = rec
        self._ctx = ctx
        #if ctx:
        #    ctx.addRecord(self)
    
    @LazyProperty
    def recname(self):
        return self._rec.getName()

    @LazyProperty
    def classes(self):
        return tuple(record.getName() for record, _ in self._rec.getSuperClasses())

    @LazyProperty
    def bases(self):
        return tuple(record.getName() for record in self._rec.getType().getClasses())
    
    @LazyProperty
    def fields(self):
        return {RecVal.getName() for RecVal in self._rec.getValues()}

    def __repr__(self):
        self.__late_init__()
        fields = {key: self.__dict__[key] for key in self.fields}
        return f"<{self._rec.getName()}: {self.bases} {fields}>"

    def __getattr__(self, key: str):
        Value = Init2Value(self._rec.getValue(key).getValue(), self._ctx)
        self.__dict__[key] = Value
        return Value

    def __late_init__(self):
        for key in self.fields:
            if key not in self.__dict__:
                self.__dict__[key] = Init2Value(self._rec.getValue(key).getValue(), self._ctx)

    @classmethod
    def check(cls, ins):
        return cls.__name__ in ins.classes

    def cast(self, cls):
        if isinstance(self, cls):
            return cls(self._rec)
        return None

    def safe_cast(self, cls) -> 'TableGenRecord':
        if isinstance(self, cls):
            return cls(self._rec)
        return self

class TypedRecord(TableGenRecord):

    @LazyProperty
    def fields(self):
        return {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}
