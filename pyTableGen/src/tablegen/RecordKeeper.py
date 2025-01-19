import tablegen.binding as binding
from tablegen.unit.record import TableGenRecord
from tablegen.unit.bits import Bits, VarBit, Unset
from tablegen.unit.dag import DAG
import weakref

from .utils import LazyAttr
from random import random
import os

def load(td: str, incDir: list[str] = list())->binding.RecordKeeper:
    return binding.ParseTableGen(td, binding.StringVector(incDir))

def loads(tds: str, incDir: list[str] = list())->binding.RecordKeeper:
    filename = hex(hash(random()))[2:]+".td"
    with open(filename, 'w') as f:
        f.write(tds)
    rec = binding.ParseTableGen(filename, binding.StringVector(incDir))
    os.remove(filename)
    return rec


class Wrapper:
    __cached__ = weakref.WeakValueDictionary()

    def __init_subclass__(cls):
        cls.__cached__ = weakref.WeakValueDictionary()

    def __new__(cls, obj, *args, **kwargs):
        if cached := cls.__cached__.get(id(obj)):
            return cached
        if issubclass(obj.__class__, TableGenRecord):
            return obj
        ins = super().__new__(cls)
        cls.__cached__[id(obj)] = ins
        return ins

class TableGenRecordWrapper(Wrapper, TableGenRecord):

    def __init__(self, rec: binding.Record):
        self._rec = rec
        self.RK = RecordKeeper(rec.getRecords())

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
        value = self.RK.getValuefromInit(self._getValueInit(key))
        if isinstance(value, Bits):
            value.name = key
        return value

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

class CacheDict:
    '''
    A CacheDict is a dictionary that provide __getf__ to get value like dict, and save result with real dict as cache.
    '''

    def __init__(self):
        self.__cache__ = dict()

    def __getf__(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        try:
            return self.__cache__[key]
        except KeyError:
            if ins := self.__getf__(key):
                self.__cache__[key] = ins
                return ins
            raise KeyError

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

class Variable:
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"

    def value(self, obj):
        return getattr(obj, self.name)

    def getName(self):
        return self.name

    def __getitem__(self, v):
        return VarBit(self, v)

class RecordKeeper(CacheDict, Wrapper):

    def __init__(self, RK: binding.RecordKeeper):
        super().__init__()
        self._RK = RK

    @classmethod
    def load(cls, td: str, incDir: list[str] = list()):
        return cls(load(td, incDir))
    
    @classmethod
    def loads(cls, tds: str, incDir: list[str] = list()):
        return cls(loads(tds, incDir))

    def getDefs(self, base=None, *clses):
        if not base:
            for rec in self._RK.getDefs():
                yield self.getRecord(rec)
        else:
            if not clses:
                if isinstance(base, type):
                    for rec in self._RK.getAllDerivedDefinitions(base.__name__):
                        if cc := self.getRecord(rec):
                            yield cc.safe_cast(base)
                        else:
                            yield None
                else:
                    for rec in self._RK.getAllDerivedDefinitions(base):
                        yield self.getRecord(rec)
            else:
                clses = [reccls if isinstance(reccls, str) else reccls.__name__ for reccls in (base, *clses)]
                for rec in self._RK.getAllDerivedDefinitions(clses):
                    yield self.getRecord(rec)

    def getValuefromInit(self, v: binding.Init) -> 'TableGenRecord | str | int | bool | Bits | VarBit | list':
        if isinstance(v, binding.IntInit):
            return v.getValue() # int
        elif isinstance(v, binding.BitInit):
            return v.getValue() # bool
        elif isinstance(v, binding.VarBitInit):
            idx = v.getBitNum()
            init = v.getBitVar()
            return VarBit(self.getValuefromInit(init), idx)
        elif isinstance(v, binding.BitsInit):
            print("get BitsInit")
            numbits = v.getNumBits()
            bitstuple = tuple([self.getValuefromInit(v.getBit(idx)) for idx in range(numbits)])
            return Bits(bitstuple)
        elif isinstance(v, binding.StringInit):
            return v.getAsUnquotedString()
        elif isinstance(v, binding.ListInit):
            return [self.getValuefromInit(e) for e in v.getValues()]
        elif isinstance(v, binding.VarInit):
            return Variable(v.getName())
        elif isinstance(v, binding.DefInit):
            if ins := self.getRecord(v.getAsString()):
                return ins
            raise ValueError(f"Record {v.getAsString()} not found")
        elif isinstance(v, binding.UnsetInit):
            print("get Unset")
            return Unset()
        elif isinstance(v, binding.DagInit):
            op = self.getValuefromInit(v.getOperator())
            kwargs = dict()
            for idx, (name, arg) in enumerate(zip(v.getArgNames(), v.getArgs())):
                if name is None:
                    kwargs[str(idx)] = self.getValuefromInit(arg)
                else:
                    kwargs[name.getAsUnquotedString()] = self.getValuefromInit(arg)
            return DAG(op, **kwargs)
        else:
            raise ValueError(f"Unknonw {v.getAsString()} {v.getKind()}")
        pass

    def __getf__(self, name_or_rec: str|binding.Record):
        if isinstance(name_or_rec, str):
            return TableGenRecordWrapper(self._RK.getDef(name_or_rec))
        else:
            return TableGenRecordWrapper(name_or_rec)

    def getRecord(self, name: str|binding.Record) -> TableGenRecord | None:
        return self[name]