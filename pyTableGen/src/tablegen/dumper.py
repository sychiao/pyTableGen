import tablegen.binding as binding
from tablegen.unit._base import TableGenType
from tablegen.unit.bits import Bits
from tablegen.unit.record import TypedRecord, TableGenRecord
from tablegen.context import TableGenContext
import inspect
import builtins

def dumpTblValue(obj: 'TableGenType|type') -> str:
    if isinstance(obj, type):
        if issubclass(obj, TableGenType):
            return obj.__class_dump__()
        else:
            match obj:
                case builtins.int:
                    return "int"
                case builtins.str:
                    return "string"
                case builtins.bool:
                    return "bool"
    else:
        if isinstance(obj, TypedRecord):
            return dumpTblRecord(obj)
        else:
            return obj.__dump__()

def dumpTblDef(obj: 'TableGenType|type[TableGenType]') -> str:
    if isinstance(obj, TableGenRecord):
        return f'''def {obj.defname} : {dumpTblRecord(obj)};'''
    elif obj.isDef() :
        if isinstance(obj, type):
            return obj.__class_dump__()
        return f'defvar {obj.defname} = {dumpTblValue(obj)};'
    raise ValueError(f'Cannot dumpTblDef {obj} without definition')

def isComplex(obj: 'TableGenType|type[TableGenType]') -> bool:
    if isinstance(obj, TableGenType):
        return obj.isComplex()
    return False

def isDef(obj: 'TableGenType|type[TableGenType]') -> bool:
    if isinstance(obj, TableGenType):
        return obj.isDef()
    return False

def dumpTblDecl(obj, name=None)->str:
    if isinstance(obj, TableGenType):
        if obj.hasName():
            if not obj.isDef() or obj.isComplex():
                return f'{dumpTblValue(obj.getType())} {obj.defname};'
            else:
                return f'{dumpTblValue(obj.getType())} {obj.defname} = {dumpTblValue(obj)};'
        raise ValueError(f'Cannot dumpTblDecl {obj} without name')
    else:
        if name:
            return f'{dumpTblValue(type(obj))} {name} = {obj};'
        raise ValueError(f'Cannot dumpTblDecl {obj} without name')
    

import textwrap

def dumpTblRecord(obj: 'TableGenRecord')->str:
    # args = [f"{dumpTblValue(ty)} {arg}" for arg, ty in obj.args()]
    add_fields = list()
    let_fields = list()
    if obj.additional_fields():
        for name, (val, _) in obj.additional_fields().items():
            add_fields.append(dumpTblDecl(val, name))
            if isinstance(val, TableGenType) and (not isDef(val) or isComplex(val)):
                let_fields.append(f"let {name} = {dumpTblValue(obj.__dict__[name])}")

    additionalBody= "{\n" + textwrap.indent("\n".join(add_fields + let_fields), '    ') + "\n}" if add_fields else ""
    args = [f"{dumpTblValue(ty)} {arg}" for arg, ty in obj.args()]
    return f"{obj.getType().__class_dump__()}<{", ".join(args)}>{additionalBody}"