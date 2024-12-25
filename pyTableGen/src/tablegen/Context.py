import tablegen.binding as binding
from tablegen.unit.record import TableGenRecord
from typing import overload, TypeVar, Generator, Tuple

class TableGenContext:

    def __init__(self, RK: binding.RecordKeeper | None = None):
        self.records = dict()
        self.classes = dict()
        self.RK = RK

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
    
    def getDefs(self, base=None, *clses): # type: ignore
        if not base:
            for rec in self.RK.getDefs():
                yield self.getRecord(rec)
        else:
            if not clses:
                if isinstance(base, type):
                    for rec in self.RK.getAllDerivedDefinitions(base.__name__):
                        yield self.getRecord(rec).safe_cast(base)
                else:
                    for rec in self.RK.getAllDerivedDefinitions(base):
                        yield self.getRecord(rec)
            else:
                clses = [reccls if isinstance(reccls, str) else reccls.__name__ for reccls in (base, *clses)]
                for rec in self.RK.getAllDerivedDefinitions(clses):
                    yield self.getRecord(rec)


    def getRecordKeeper(self) -> binding.RecordKeeper:
        return self.RK

    def addRecord(self, recobj):
        self.records[recobj.recname] = recobj
        return recobj

    def getRecord(self, name_or_rec) -> TableGenRecord:
        if isinstance(name_or_rec, str):
            name = name_or_rec
            if ret := self.records.get(name):
                return ret
            if self.RK:
                return self.addRecord(TableGenRecord(self.RK.getDef(name), self))
        elif isinstance(name_or_rec, binding.Record):
            rec = name_or_rec
            if ret := self.records.get(rec):
                return ret
            if self.RK:
                return self.addRecord(TableGenRecord(rec, self))
