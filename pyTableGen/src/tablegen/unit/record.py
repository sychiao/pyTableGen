from dataclasses import dataclass, is_dataclass
from typing import ClassVar, Any
import typing

from ._base import TableGenType, MetaTableGenType
from ..utils import LazyAttr

class _TableGenRecord:
    '''
    Magic methods for TableGenRecord for override
    '''
    def __fields__(self)->set[str]:
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

    def cast[T](self, cls: type[T]) -> T:
        return self # type: ignore

import inspect

class RecordDumpable:

    def args(self):
        raise NotImplementedError

    def additional_fields(self):
        raise NotImplementedError

class TypedRecord(TableGenRecord):

    @LazyAttr
    def __fields__(self):
        # ClassVar is not a field
        return {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}

    def __classes__(self) -> tuple[str, ...]:
        return tuple(cls.__name__ for cls in type(self).__mro__ if issubclass(cls, TypedRecord))

    def __base__(self) -> tuple[str, ...]:
        return (type(self).__name__, )

    def __items__(self) -> dict[str, Any]:
        return {key: self.__dict__[key] for key in self.fields}

    def __setattr__(self, name: str, value: Any, /) -> None:
        print("TypedRecord SetAttr", name, value)
        if isinstance(value, TableGenType):
            value.bind(name, self)
        return super().__setattr__(name, value)

    def args(self):
        s = inspect.get_annotations(self.getType().__init__)
        return [(key, ty) for key, ty in s.items() if key in self.fields]

    def additional_fields(self) -> dict[str, tuple[Any, type]]:
        # fields is lazy attribute so it must be called first before iterate __dict__
        fields = self.fields 
        return {k: (self.__dict__[k], v.getType() if issubclass(type(v), TableGenType) else type(v))
                    for k, v in self.__dict__.items() if not k.startswith("_") and k not in fields}
    
    def let(self, key, value):
        setattr(self, key, value)
        return self

