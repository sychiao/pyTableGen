import tablegen.binding as binding
from typing import overload, TypeVar, Generator, Tuple

from .unit.record import TableGenRecord
from .RecordKeeper import RecordKeeper

class TableGenContext:

    def __init__(self, RK: RecordKeeper | None = None):
        self.records = dict()
        self.classes = dict()
        self.RK = RK
        self.defscounter = 0
        self.defs = set()

    @overload
    def getDefs()-> Generator[TableGenRecord, None, None]: # type: ignore
        ... # pragma: no cover

    T = TypeVar('T')
    @overload
    def getDefs(self, base: type[T]) -> Generator[T, None, None]: # type: ignore
        ... # pragma: no cover

    @overload
    def getDefs(self, base: str|type, *clses: Tuple[str|type, ...]) -> Generator[TableGenRecord, None, None]:
        ... # pragma: no cover

    def getDefs(self, base=None, *clses): # type: ignore
        if self.RK:
            yield from self.RK.getDefs(base, *clses)
        if base:
            clses = [self.getClass(reccls) if isinstance(reccls, str) else reccls for reccls in (base, *clses)]
            for defname in self.defs:
                rec = self.records[defname]
                if all(isinstance(rec, reccls) for reccls in clses):
                    yield rec

    def getRecordKeeper(self) -> binding.RecordKeeper:
        return self.RK

    def __get_noname(self):
        self.defscounter += 1
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

    def getRecord(self, name) -> TableGenRecord | None:
        if ret := self.records.get(name):
            return ret
        if self.RK:
            return self.RK.getRecord(name)
