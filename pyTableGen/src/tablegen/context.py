import tablegen.binding as binding
from typing import overload, TypeVar, Generator, Tuple

from .unit.record import TableGenRecord
from .wrapper.recordkeeper import RecordKeeper

class Context:
    
    def _get(self, name):
        raise NotImplementedError # pragma: no cover

    @property
    def get(self):
        # 'Getter, TypedGetter' is a class to trick to typing "get[A](name)"
        return Getter(self)

class TypedGetter[T]:

    def __init__(self, ctx: Context, cls: type[T]):
        self.ctx = ctx
        self.cls = cls

    def __call__(self, name: str, default_value=None) -> T | None:
        if rec := self.ctx._get(name):
            return rec.cast(self.cls)
        return default_value

class Getter:

    def __init__(self, ctx: Context):
        self.ctx = ctx

    def __getitem__[T](self, item: type[T]) -> TypedGetter[T]:
        return TypedGetter(self.ctx, item)

    def __call__(self, name: str, default_value=None) -> TableGenRecord | None:
        if rec := self.ctx._get(name):
            return rec
        return default_value

class TableGenContext(Context):

    @staticmethod
    def load(td: str, incDir: list[str] = list()) -> 'TableGenContext':
        from .wrapper.recordkeeper import RecordKeeper
        RK = RecordKeeper.load(td, incDir)
        return TableGenContext(RK)

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

    def getClass(self, name: str):
        if self.RK and (recls := self.RK.getClass(name)):
            return recls

    def getDefs(self, base=None, *clses): # type: ignore
        if self.RK:
            yield from self.RK.getDefs(base, *clses)
        if base:
            clses = [self.getClass(reccls) if isinstance(reccls, str) else reccls for reccls in (base, *clses)]
            for defname in self.defs:
                rec = self.records[defname]
                if all(isinstance(rec, reccls) for reccls in clses):
                    yield rec

    def getRecordKeeper(self) -> RecordKeeper | None:
        return self.RK

    def __get_noname(self):
        self.defscounter += 1
        return f'__noname{self.defscounter}'

    def __setattr__(self, name: str, value, /) -> None:
        if isinstance(value, TableGenRecord):
            self.addDef(value, name)
        else:
            super().__setattr__(name, value)

    def addDef(self, recobj, name=None):
        name = name or self.__get_noname()
        if name not in self.defs:
            self.records[name] = recobj.bind(name, self)
            self.defs.add(name)
        else:
            raise ValueError(f"Record {name} already exists")

    def _get(self, name):
        if ret := self.records.get(name):
            return ret
        if self.RK:
            if rec := self.RK.getRecord(name):
                return rec.bind(name, self)

    def __getattr__(self, name) -> TableGenRecord:
        if rec := self.getRecord(name):
            return rec
        elif reccls := self.getClass(name):
            return reccls
        raise AttributeError(f"Record {name} not found")

    @property
    def getRecord(self):
        '''
        Get a record from the context, if the record is not found, it will raise a KeyError
        '''
        return self.get

    @property
    def getdef(self):
        return self.getRecord