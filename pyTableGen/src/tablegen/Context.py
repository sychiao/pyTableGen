import tablegen.binding as binding
from typing import overload, TypeVar, Generator, Tuple

from .unit.bits import Bits
from .unit.record import TableGenRecord, TableGenRecordWrapper

class RecordKeeper(binding.RecordKeeper):
    
    def getRKRecord(self, name_or_rec) -> TableGenRecord | None:
        if isinstance(name_or_rec, str):
            rec = self.RK.getDef(name_or_rec)
        else:
            rec = name_or_rec
        wrappedrec = TableGenRecordWrapper(rec)
        wrappedrec.setCtx(self)
        return self.addRecord(wrappedrec)

    def getRKClass(self, name_or_rec: str) -> type[TableGenRecord]:
        # TODO: Implement
        return TableGenRecord

class TableGenContext:

    def __init__(self, RK: binding.RecordKeeper | None = None):
        self.records = dict()
        self.classes = dict()
        self.RK = RK
        self.defscounter = 0
        self.defs = set()

    def getValuefromInit(self, v: binding.Init):
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
            return [self.getValuefromInit(e) for e in v.getValues()]
        elif isinstance(v, binding.DefInit):
            return TableGenRecordWrapper(v.getDef())
        elif isinstance(v, binding.DagInit):
            return "DAG"
        else:
            return f"Unknonw {v.getAsString()}"
        pass

    @overload
    def getDefs()-> Generator[TableGenRecord, None, None]: # type: ignore
        ...

    T = TypeVar('T')
    @overload
    def getDefs(self, base: type[T]) -> Generator[T, None, None]: # type: ignore
        ...

    @overload
    def getDefs(self, base: str|type, *clses: Tuple[str|type, ...]) -> Generator[TableGenRecord, None, None]:
        ...

    def getRKDefs(self, base=None, *clses): # type: ignore
        if self.RK:
            if not base:
                for rec in self.RK.getDefs():
                    yield self.getRecord(rec)
            else:
                if not clses:
                    if isinstance(base, type):
                        for rec in self.RK.getAllDerivedDefinitions(base.__name__):
                            if cc := self.getRecord(rec):
                                yield cc.safe_cast(base)
                            else:
                                yield None
                    else:
                        for rec in self.RK.getAllDerivedDefinitions(base):
                            yield self.getRecord(rec)
                else:
                    clses = [reccls if isinstance(reccls, str) else reccls.__name__ for reccls in (base, *clses)]
                    for rec in self.RK.getAllDerivedDefinitions(clses):
                        yield self.getRecord(rec)

    def getDefs(self, base=None, *clses): # type: ignore
        yield from self.getRKDefs(base, *clses)
        if base:
            clses = [self.getClass(reccls) if isinstance(reccls, str) else reccls for reccls in (base, *clses)]
            for defname in self.defs:
                rec = self.records[defname]
                if all(isinstance(rec, reccls) for reccls in clses):
                    yield rec

    def getRecordKeeper(self) -> binding.RecordKeeper:
        return self.RK

    def getClass(self, name_or_rec: str) -> type[TableGenRecord]:
        if isinstance(name_or_rec, str):
            name = name_or_rec
            if ret := self.classes.get(name):
                return ret
        elif isinstance(name_or_rec, binding.Record):
            pass
        
        return TableGenRecord

    def __get_noname(self):
        return f'__noname{self.defscounter}'

    def addDef(self, recobj, name=None):
        name = name or self.__get_noname()
        if name not in self.defs:
            self.records[name] = recobj
            self.defs.add(name)
        else:
            raise ValueError(f"Record {name} already exists")

    def addRecord(self, recobj):
        # self.cls2rec
        self.records[recobj.recname] = recobj
        return recobj

    def getRKRecord(self, name_or_rec) -> TableGenRecord | None:
        if self.RK:
            if isinstance(name_or_rec, str):
                rec = self.RK.getDef(name_or_rec)
            else:
                rec = name_or_rec
            wrappedrec = TableGenRecordWrapper(rec)
            wrappedrec.setCtx(self)
            return self.addRecord(wrappedrec)

    def getRecord(self, name_or_rec) -> TableGenRecord | None:
        if isinstance(name_or_rec, str):
            name = name_or_rec
        elif isinstance(name_or_rec, binding.Record):
            name = name_or_rec.getName()
        else:
            raise TypeError(f"Invalid type {type(name_or_rec)}")
        if ret := self.records.get(name):
            return ret
        if self.RK:
            return self.getRKRecord(name_or_rec)
