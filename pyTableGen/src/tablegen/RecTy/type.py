from ..binding import IntInit, StringInit, ListInit, DefInit
import tablegen.binding as binding
import weakref
from typing import ClassVar
import typing

class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __getitem__(cls, arg):
        clsname = f'{cls.__name__}[{arg}]'
        try:
            return cls.__types__[clsname]
        except KeyError:
            cls.__types__[clsname] = type(f'{cls.__name__}[{arg}]', (cls,), {'Args': arg})
            return cls.__types__[clsname]

    def __instancecheck__(cls, instance, /) -> bool:
        print('instance check', cls.__name__, cls.check(instance))
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)

class TableGenType(metaclass=MetaTableGenType):
    pass

class Bits(TableGenType):
    Length = -1

    def __init__(self, bits):
        self.bits = bits
    
    def __repr__(self):
        return f'{self.__class__.__name__}({self.bits})'

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
        if ctx and (ins := ctx.getRecord(obj.getName())):
            return ins
        elif cached := cls.__cached__.get(id(obj)):
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
        if ctx:
            ctx.addRecord(self)
    
    @property
    def recname(self):
        try:
            return self._name
        except:
            self._name = self._rec.getName()
            return self._name

    @property
    def classes(self):
        try:
            return self._classes
        except:
            self._classes = tuple(record.getName() for record, _ in self._rec.getSuperClasses())
            return self._classes

    @property
    def bases(self):
        try:
            return self._base
        except:
            self._base = tuple(record.getName() for record in self._rec.getType().getClasses())
            return self._base

    def __repr__(self):
        self.__late_init__()
        fields = {key: self.__dict__[key] for key in self.fields()}
        return f"<{self._rec.getName()}: {self.bases} {fields}>"

    def __getattr__(self, key: str):
        Value = Init2Value(self._rec.getValue(key).getValue(), self._ctx)
        self.__dict__[key] = Value
        return Value

    def fields(self):
        try:
            return self._fields
        except:
            self._fields = {RecVal.getName() for RecVal in self._rec.getValues()}
            return self._fields

    def __late_init__(self):
        for key in self.fields():
            if key not in self.__dict__:
                self.__dict__[key] = Init2Value(self._rec.getValue(key).getValue(), self._ctx)

    @classmethod
    def check(cls, ins):
        return cls.__name__ in getattr(ins, "_classes", [])

    def cast(self, cls):
        if isinstance(self, cls):
            return cls(self._rec)
        return None

class TypedRecord(TableGenRecord):

    def fields(self):
        try:
            return self._fields
        except:
            self._fields = {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}
            return self._fields

class dag:
    pass

class ValueType(TypedRecord):
    Namespace: str
    Size: int
    Value: int

class RegisterClass(TypedRecord):
    Namespace: str
    RegTypes: list[ValueType]
    Size: int
    MemberList: dag
