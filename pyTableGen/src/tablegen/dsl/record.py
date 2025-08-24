from collections.abc import Sequence, Mapping
from typing import Any, overload, Self
import inspect
from types import new_class
from tablegen.unit.value import UnknownValue
import copy

class TblRecMetaData:
    '''
    Here is the metadata for tablegen record
    class {name} <{signature}> : {bases} {
        {fields}
    }
    def {name} : {recs: cls<{args}>} {
        {extra}
    }
    '''
    name: str
    signature: tuple[str, ...]
    fields: dict[str, type]
    bases: tuple[str, ...]
    args: tuple[Any, ...]
    kwargs: dict[str, Any]
    recs: tuple[Any, ...]
    extra: dict[str, Any] | None
    

    def __init__(self):
        self.name = ""
        self.signature = tuple()
        self.fields = dict()
        self.bases = tuple()
        self.tdrec = None
        self.args = tuple()
        self.kwargs = dict()
        self.recs = tuple()
        self.extra = None

class RecType(type):
    '''
    RecType is a metaclass for TableGen Record.
    which initilize with
    __new__ create a new class with TblRecMetaData
    __init_subclass__ update the metadata with customize
    __init__ update the metadata with rules
      1. if fields is empty, use __annotations__ as fields
      2. if bases has _tbl_metadata, merge the fields
      3. signature is the parameters of __init__ method
    __call__ create a new instance, and let extra as dict
    '''

    def __eq__(self, ty):
        return True
    
    @property
    def tbl(self) -> TblRecMetaData:
        return self._tbl_metadata
    
    def __new__(mcls, name, bases, attrs, **kwds):
        cls = super().__new__(mcls, name, bases, attrs, **kwds)
        cls._tbl_metadata = TblRecMetaData()
        return cls
    
    def __init__(self, name, bases, attrs, **kwds):
        super().__init__(name, bases, attrs, **kwds)
        if not self.tbl.fields:
            self.tbl.fields = self.__annotations__ if hasattr(self, '__annotations__') else {}
        for base in bases:
            if hasattr(base, '_tbl_metadata') and base._tbl_metadata:
                self.tbl.fields |= base._tbl_metadata.fields
        if not self.tbl.signature and hasattr(self, '__init__'):
            sig = [(name, param.annotation) for name, param in inspect.signature(self.__init__).parameters.items()]
            self.tbl.signature = tuple(sig[1:])

    def __call__(self, *args, **kwds):
        ins = super().__call__(*args, **kwds)
        ins.tbl.extra = ins.tbl.extra or {}
        return ins
    
    def __instancecheck__(self, instance: Any) -> bool:
        if issubclass(type(instance), _Record):
            for rec in instance.recs:
                if issubclass(type(rec), self):
                    return True
        return False

class _Record(metaclass=RecType):
    # _tbl_metadata: TblRecMetaData | None = None

    @property
    def tbl(self) -> TblRecMetaData:
        return self._tbl_metadata or TblRecMetaData()

    @property
    def recs(self):
        return (self,)

    @property
    def classes(self):
        return tuple(type(rec) for rec in self.recs)

    @property
    def fields(self):
        fields = {}
        for rec in self.recs:
            fields.update(rec.tbl.fields)
        return fields
        
    def __or__(self, other):
        if isinstance(other, _Record):
            return UnionRecord(*self.recs, *other.recs)
        raise NotImplementedError
    
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._tbl_metadata = copy.copy(cls.tbl)
        instance.tbl.args = args
        instance.tbl.kwargs = kwargs
        return instance

    def __setattr__(self, name: str, value) -> None:
        if self.tbl.extra is not None:
            if not (name.startswith('_') and name.endswith('__')) \
               and not name.startswith('_tbl'):
                self.tbl.extra[name] = value
        super().__setattr__(name, value)

class TDRecord(_Record):

    def __init_subclass__(cls, metadata=None) -> None:
        print("Init TDRecord", cls, metadata)
        if metadata:
            cls.tbl.fields = metadata.fields

    def __init__(self, *args, **kwargs) -> None:
        print("Create TDRecord", self.tbl.name, args, kwargs)
        if (len(self.tbl.signature) != len(args) + len(kwargs)):
            raise TypeError(f"{self.tbl.name} takes {len(self.tbl.signature)} arguments, got {len(args) + len(kwargs)}")
        for field, ty in self.tbl.fields.items():
            setattr(self, field, UnknownValue(ty))

    @classmethod
    def create(cls):
        print([None] * len(cls.tbl.signature))
        return cls(*([None] * len(cls.tbl.signature)))
    

    
    def __repr__(self) -> str:
        lst = []
        for name, value in self.__dict__.items():
            if name in self.tbl.fields:
                if isinstance(value, _Record):
                    lst.append(f"{name}={value.__class__.__name__}(obj={hex(id(value))})")
                else:
                    lst.append(f"{name}={value!r}")
        return f"{self.__class__.__name__}(obj={hex(id(self))})" + \
                f"{{{', '.join(lst)}}}"
    
    def __dump__(self):
        raise TypeError("TDRecord cannot be dumped directly")

def UnionTDRecord(*tys : type[TDRecord], cache = dict()):
    tyset = list(sorted({ty.__name__:ty for ty in tys}.values(), key=lambda x: x.__name__))
    name = "U_" + "_OR_".join(ty.__name__ for ty in tys)
    try:
        return cache[name]
    except KeyError:
        cache[name] = new_class(name, tuple(tyset))
        tbl: TblRecMetaData = cache[name].tbl
        tbl.signature = tuple()
        tbl.fields = {}
        for ty in tyset:
            tbl.fields |= ty.tbl.fields
        return cache[name]

class PyRecord(_Record):

    def __init_subclass__(cls, TDRecord=None) -> None:
        if TDRecord and cls == TDRecord:
            raise TypeError(f"TDRecord must be the same as cls, got {TDRecord} and {cls}")
        cls.tbl.tdrec = TDRecord

    def __repr__(self) -> str:
        if self.tbl.kwargs:
            return f'''PyRecord({", ".join(f"{k}={v!r}" for k, v in self.tbl.kwargs.items())})'''
        else:
            return f'''PyRecord({", ".join(self.tbl.args)})'''

    @overload
    def __or__[*T](self, other: 'UnionRecord[*T]') -> 'UnionRecord[Self, *T]':
        ...

    @overload
    def __or__[T](self, other: T) -> 'UnionRecord[Self, T]':
        ...

    def __or__(self, other):
        return super().__or__(other)

class UnionRecord[*K](_Record):
    _recs: tuple[PyRecord]

    def __init__(self, *recs: _Record):
        self._recs = recs
        for rec in recs:
            self.__dict__.update(rec.__dict__)
            self.tbl.fields |= rec.tbl.fields

    @property
    def recs(self):
        return self._recs

    def __repr__(self):
        return f"UnionRecord({', '.join(repr(rec) for rec in self.recs)})"

    @overload
    def __or__[*T](self, other: 'UnionRecord[*T]') -> 'UnionRecord[*K, *T]':...
    
    @overload
    def __or__[T](self, other: T) -> 'UnionRecord[*K, T]':...

    def __or__(self, other) :
        return super().__or__(other)

