from typing import ClassVar, Any, Self
import typing
import inspect

from ._base import TableGenType
from .value import Unset
from .bits import Bits
from ..utils import LazyAttr

class _TableGenRecord:
    '''
    Magic methods for TableGenRecord for override
    '''
    def __fields__(self)->dict[str, type|TableGenType]:
        raise NotImplementedError(f"{type(self)} __fields__ is not NotImplemented") # pragma: no cover

    def __base__(self)->tuple[str, ...]:
        raise NotImplementedError(f"{type(self)} __base__ is not NotImplemented") # pragma: no cover
    
    def __classes__(self)->tuple[str, ...]:
        raise NotImplementedError(f"{type(self)} __classes__ is not NotImplemented") # pragma: no cover

    def __items__(self)->dict[str, Any]:
        raise NotImplementedError(f"{type(self)} __items__ is not NotImplemented") # pragma: no cover

class TableGenRecord(_TableGenRecord, TableGenType):

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
        return self.__items__()

    @classmethod
    def check(cls, ins):
        return issubclass(ins.__class__, TableGenRecord)

    def __repr__(self):
        return f"<{self.defname}: {self.bases} {self.items}>"

    def __call__(self, *args) -> 'TableGenRecord' :
        raise ValueError(f"TableGenRecord {self.defname} is not callable, only TableGenClassWrapper is callable")

    def cast[T](self, cls: type[T]) -> T:
        return self # type: ignore

    def __setattr__(self, name: str, value: Any, /) -> None:
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            if '__reset_field__' in self.__dict__:
                if name in self.items:
                    self.__reset_field__.add(name)
            if not name.startswith('_') and isinstance(value, TableGenType):
                if not value.hasName():
                    value.bind(name, self)
            super().__setattr__(name, value)

    def __getitem__(self, key: str) -> Any:
        if key not in self.__dict__:
            self.__dict__[key] = self._getValue(key)
        return self.__dict__[key]

    def __items__(self) -> dict[str, Any]:
        dctA = {key: getattr(self, key, None) for key in self.fields}
        dctB = {key: val for key, val in self.__dict__.items() if not key.startswith("_")}
        return {**dctA, **dctB}

    def additional_fields(self) -> dict[str, tuple[Any, type]]:
        # fields is lazy attribute so it must be called first before iterate __dict__
        fields = self.fields
        return {k: (v, v.geType() if isinstance(v, TableGenRecord) else type(v)) 
                              for k, v in self.items.items() if k not in fields}
    
    def let_fields(self)->dict[str, Any]:
        return {name: getattr(self, name) for name in self.__reset_field__}

    def let(self, key, value):
        setattr(self, key, value)
        return self
    
    def decl(self, name, type):
        pass

        
class TableGenDummyRecord(TableGenRecord):
    '''
    TableGenDummyRecord is a dummy record for TableGenRecord which class is defined inside TableGen
    '''
    __record_class__: TableGenRecord

    def __init__(self, regclass, *args, **kwargs):
        self.__record_class__ = regclass
        self.__record_args__ = args

    def __fields__(self):
        return {e: t for e, t in self.__record_class__.fields.items() if ':' not in e}

    def __base__(self):
        return (self.__record_class__.defname, )

    def __repr__(self):
        return f"<{self.defname} : {self.bases[0]}<{', '.join(map(str, self.__record_args__))}> {self.fields}>"

    def __def_dump__(self):
        ret = f"def {self.defname} : {self.bases[0]}<{', '.join(map(str, self.__record_args__))}>"
        if self.additional_fields() or self.let_fields():
            ret += " {"
            for name, (value, ty) in self.additional_fields().items():
                ret += f"\n    {ty.__class_dump__()} {name};"
            for name, (value, _) in self.additional_fields().items():
                if isinstance(value, Bits) and name == value.defname:
                    # skip the value if it's a bits without init value
                    continue
                elif isinstance(value, Unset):
                    # skip the value if it's a unset value
                    continue
                ret += f"\n    let {name} = {value.__dump__()};"
            for name, value in self.let_fields().items():
                ret += f"\n    let {name} = {value.__dump__()};"
            ret += "\n}"
        else:
            ret += ";"
        return ret


class TypedRecord(TableGenRecord):

    @LazyAttr
    def __fields__(self):
        # ClassVar is not a field
        return {key: ty for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}

    def __classes__(self) -> tuple[str, ...]:
        return tuple(cls.__name__ for cls in type(self).__mro__ if issubclass(cls, TypedRecord))

    def __base__(self) -> tuple[str, ...]:
        return (type(self).__name__, )

    def args(self):
        s = inspect.get_annotations(self.getType().__init__)
        return [(key, ty) for key, ty in s.items() if key in self.fields]

