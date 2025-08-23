from typing import Iterable
import tablegen.binding as binding
from tablegen.unit.record import TableGenRecord
from tablegen.unit.bits import Bits, VarBit, Unset
from tablegen.unit.dag import DAG
from tablegen.wrapper.wrapper import Wrapper
from ..utils import CacheDict
from random import random
import os

from ..unit.operator import Operator, Add
import tablegen.unit.operator as op

from .record import TableGenClassWrapper, TableGenRecordWrapper

def load(td: str, incDir: list[str] = list())->binding.RecordKeeper:
    return binding.ParseTableGen(td, binding.StringVector(incDir))

def loads(tds: str, incDir: list[str] = list())->binding.RecordKeeper:
    filename = hex(hash(random()))[2:]+".td"
    with open(filename, 'w') as f:
        f.write(tds)
    rec = binding.ParseTableGen(filename, binding.StringVector(incDir))
    os.remove(filename)
    return rec

class Variable:
    def __init__(self, name: str):
        self.name = name
    
    def __repr__(self):
        return f"Var({self.name})"
    
    def __repr__(self):
        if ":" in self.name:
            _, name = self.name.split(":")
        else:
            name = self.name
        return name

    def value(self, obj):
        return getattr(obj, self.name)

    def getName(self):
        return self.name

    @property
    def defname(self):
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

    def _getDefs(self, recs: Iterable[binding.Record]) :
        for rec in recs:
            if r :=  self.getRecord(rec):
                yield r
            else:
                raise ValueError(f"Record {rec.getName()} not found")

    def getDefs(self, base: str | type[TableGenRecord] | None = None, *clses) -> Iterable[TableGenRecord]:
        try:
            if not base:
                yield from self._getDefs(self._RK.getDefs().values())
            else:
                if not clses:
                    if isinstance(base, type):
                        for r in self._getDefs(self._RK.getAllDerivedDefinitions(base.__name__)):
                            yield r.cast(base)
                    else:
                        yield from self._getDefs(self._RK.getAllDerivedDefinitions(base))
                else:
                    clses = [reccls if isinstance(reccls, str) else reccls.__name__ for reccls in (base, *clses)]
                    yield from self._getDefs(self._RK.getAllDerivedDefinitions(clses))
        except ValueError as e:
            raise e

    def getValuefromRecTy(self, t: binding.RecTy) -> 'TableGenClassWrapper | type[str] | type[int] | type[bool] | type[Bits] | type[VarBit] | type[Variable] | type[Unset] | type[DAG] | type[list]':
        if isinstance(t, binding.BitRecTy):
            return bool
        elif isinstance(t, binding.IntRecTy):
            return int
        elif isinstance(t, binding.StringRecTy):
            return str
        elif isinstance(t, binding.ListRecTy):
            return list
        elif isinstance(t, binding.DagRecTy):
            return DAG
        elif isinstance(t, binding.BitsRecTy):
            return Bits
        elif isinstance(t, binding.RecordRecTy):
            record = t.getClasses()[0]
            return TableGenClassWrapper(record, self)
        else:
            raise ValueError(f"Unknonw {t.getAsString()} {t.getKind()}")

    def getVarBitInit(self, v: binding.VarBitInit) -> VarBit:
        return VarBit(self.getValuefromInit(v.getBitVar()), v.getBitNum())

    def getBitsInit(self, v: binding.BitsInit) -> Bits:
        numbits = v.getNumBits()
        bitstuple = tuple([self.getValuefromInit(v.getBit(idx)) for idx in range(numbits)])
        return Bits(bitstuple)

    def getDagInit(self, v: binding.DagInit) -> DAG:
        op = self.getValuefromInit(v.getOperator())
        kwargs = dict()
        for idx, (name, arg) in enumerate(zip(v.getArgNames(), v.getArgs())):
            if name is None:
                kwargs[str(idx)] = self.getValuefromInit(arg)
            else:
                kwargs[name.getAsUnquotedString()] = self.getValuefromInit(arg)
        return DAG(op, **kwargs)

    def getValuefromInit(self, v: binding.Init) -> 'TableGenRecord | Operator | str | int | bool | Bits | VarBit | Variable | Unset | DAG | list':
        if isinstance(v, binding.IntInit):
            return v.getValue() # int
        elif isinstance(v, binding.BitInit):
            return v.getValue() # bool
        elif isinstance(v, binding.VarBitInit):
            return self.getVarBitInit(v)
        elif isinstance(v, binding.BitsInit):
            return self.getBitsInit(v)
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
            return Unset(None)
        elif isinstance(v, binding.DagInit):
            return self.getDagInit(v)
        elif isinstance(v, binding.UnOpInit):
            if v.getOpcode() == binding.UnaryOp.NOT:
                return op.Not(self.getValuefromInit(v.getOperand()))
            return f"Operator({v.getOpcode()}, {self.getValuefromInit(v.getOperand())})"
        elif isinstance(v, binding.BinOpInit):
            if v.getOpcode() == binding.BinaryOp.ADD:
                # Special case for Add operator
                return Add(self.getValuefromInit(v.getLHS()), self.getValuefromInit(v.getRHS()))
            return f"Operator(\
                {v.getOpcode()},\
                {self.getValuefromInit(v.getLHS())},\
                {self.getValuefromInit(v.getRHS())}\
            )"
        else:
            return f"Unknonw {v.getAsString()} {v.getKind()}"

    def getClass(self, name: str) -> TableGenRecord | None:
        return TableGenClassWrapper(self._RK.getClass(name), self)
    
    def getClasses(self) -> dict[str, TableGenRecord]:
        dct = {name: TableGenClassWrapper(cls, self) 
               for name, cls in self._RK.getClasses().items()}
        return dct

    def __getf__(self, name_or_rec: str|binding.Record): # magic method of CacheDict
        if isinstance(name_or_rec, str):
            if rec := self._RK.getDef(name_or_rec):
                return TableGenRecordWrapper(rec, self)
            else:
                return None
        else:
            return TableGenRecordWrapper(name_or_rec, self)

    def getRecord(self, name: str|binding.Record) -> TableGenRecord | None:
        return self.get(name, None) # use __getitem__ of CacheDict

    def __getattr__(self, name: str):
        return self.getRecord(name)
