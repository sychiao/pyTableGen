from typing import ClassVar, Any
import typing

from ._base import TableGenType
from ..utils import LazyAttr

class _TableGenRecord:
    '''
    Magic methods for TableGenRecord for override
    '''
    def __fields__(self)->set[str]:
        raise NotImplementedError # pragma: no cover

    def __base__(self)->tuple[str, ...]:
        raise NotImplementedError # pragma: no cover
    
    def __classes__(self)->tuple[str, ...]:
        raise NotImplementedError # pragma: no cover

    def __item__(self)->dict[str, Any]:
        raise NotImplementedError # pragma: no cover

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
        return self.__item__()

    @classmethod
    def check(cls, ins):
        return issubclass(ins.__class__, TableGenRecord)

    def __repr__(self):
        return f"<{self.defname}: {self.bases} {self.items}>"

    def cast[T](self, cls: type[T]) -> T:
        return self # type: ignore

class TypedRecord(TableGenRecord):

    @LazyAttr
    def __fields__(self):
        return {key for key, ty in type(self).__annotations__.items() if typing.get_origin(ty) != ClassVar}

    def __classes__(self) -> tuple[str, ...]:
        return tuple(cls.__name__ for cls in type(self).__mro__ if issubclass(cls, TypedRecord))

    def __base__(self) -> tuple[str, ...]:
        return (type(self).__name__, )

    def __item__(self) -> dict[str, Any]:
        return {key: self.__dict__[key] for key in self.fields}
