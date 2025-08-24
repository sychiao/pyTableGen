from typing import Iterable
import tablegen.binding as binding
from tablegen.unit.record import TableGenRecord, TableGenDummyRecord
from tablegen.unit.bits import Bits, VarBit, Unset
from tablegen.unit.dag import DAG
import weakref

from tablegen.wrapper.wrapper import Wrapper

from ..utils import LazyAttr, CacheDict


class TableGenRecordWrapper(Wrapper, TableGenRecord):
    __typed__ = dict()

    def __init__(self, rec: binding.Record, RK=None):
        self.__recname__ = rec.getName()
        self._rec = rec
        self._RK = RK
    
    @property
    def RK(self):
        if self._RK is None:
            raise AttributeError("RecordKeeper is not set, donot support to access fields")
        return self._RK

    def setRecordKeeper(self, RK):
        self._RK = RK

    def getBaseClasses(self):
        return [self.RK.getClass(cls_name) for cls_name in self.bases]

    def __classes__(self):
        return tuple(record.getName() for record, _ in self._rec.getSuperClasses())

    def __base__(self):
        return tuple(record.getName() for record in self._rec.getType().getClasses())

    def __fields__(self):
        return {RecVal.getName(): self.RK.getValuefromRecTy(RecVal.getType()) for RecVal in self._rec.getValues()}

    def __items__(self):
        return {key: self.__dict__[key] for key in self.fields}

    def _getValueInit(self, key: str):
        if v := self._rec.getValue(key):
            return v.getValue()
        raise AttributeError(f"Record {self.__recname__} has no attribute {key}")

    def _getValue(self, key: str):
        value = self.RK.getValuefromInit(self._getValueInit(key))
        return value.bind(key) if isinstance(value, Bits) else value

    def __getattr__(self, key: str):
        if key not in self.__dict__:
            self.__dict__[key] = self._getValue(key)
        return self.__dict__[key]
    
    def __getitem__(self, key: str):
        if key not in self.__dict__:
            self.__dict__[key] = self._getValue(key)
        return self.__dict__[key]

    def __late_init__(self):
        for key in self.fields:
            if key not in self.__dict__:
                self.__dict__[key] = self._getValue(key)

    @classmethod
    def getTypedWrapper(cls, typedcls):
        if typedcls not in cls.__typed__:
            cls.__typed__[typedcls] = \
                type(f'{typedcls.__name__}Wrapper', 
                       (TableGenRecordWrapper, typedcls), {})
        return cls.__typed__[typedcls]

    def cast(self, cls, default_val = None):
        if isinstance(self, cls):
            return TableGenRecordWrapper.getTypedWrapper(cls)(self._rec, self.RK)
        return default_val

class TableGenClassWrapper(TableGenRecordWrapper):
    
    @property
    def __name__(self):
        return self.__recname__

    def args(self):
        args = dict()
        for init in self._rec.getTemplateArgs():
            name = init.getAsUnquotedString()
            keyname = name.replace(":", "_")
            args[keyname] = self.RK.getValuefromRecTy(self._rec.getValue(name).getType())
        return args        
    
    def __late_init__(self):
        pass

    def __items__(self):
        raise TypeError("TableGenClassWrapper object is not iterable")

    def __call__(self, *args):
        print(self.args())
        return TableGenDummyRecord(self, *args)

    def __repr__(self):
        argstr = "<" + ', '.join(f'{ty.__name__} {name}' for name, ty in self.args().items()) + ">" if self.args() else ""
        fieldstr = ', '.join(f'{ty.__name__} {name}' for name, ty in self.fields.items() if ':' not in name)
        return f"tblwrapper({self.__recname__}){argstr}{{{fieldstr}}}" \

# TableGenRecord

