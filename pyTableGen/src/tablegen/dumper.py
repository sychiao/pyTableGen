import tablegen.binding as binding
from tablegen.unit._base import TableGenType
from tablegen.unit.bits import Bits
from tablegen.context import TableGenContext

def dumpTblValue(obj: 'TableGenType|type[TableGenType]') -> str:
    if isinstance(obj, type):
        return obj.__class_dump__()
    return obj.__dump__()

def dumpTblDef(obj: 'TableGenType|type[TableGenType]') -> str:
    if obj.isDef() :
        if isinstance(obj, type):
            return obj.__class_dump__()
        return f'defvar {obj.defname} = {dumpTblValue(obj)};'
    raise ValueError(f'Cannot dumpTblDef {obj} without definition')

def dumpTblDecl(obj)->str:
    if obj.hasName():
        if not obj.isDef() or obj.isComplex():
            return f'{dumpTblValue(obj.getType())} {obj.defname};'
        else:
            return f'{dumpTblValue(obj.getType())} {obj.defname} = {dumpTblValue(obj)};'
    raise ValueError(f'Cannot dumpTblDecl {obj} without name')