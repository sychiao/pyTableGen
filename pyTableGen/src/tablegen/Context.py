import tablegen.binding as binding
from typing import Type
from .Units import TableGenType
from .Units import TableGenField, TableGenRecord, TableGenClass, dag, bit, Var, BinOP

'''
class TableGenContext:
    def __init__(self, RK: binding.RecordKeeper):
        self.recordkeeper = RK
    
    def getClasses(self):
        pass

    def getDefswithClass(self, cls):
        return (cls(rec) for rec in self.recordkeeper.getAllDerivedDefinitions(cls.__name__))
'''



class TableGenContext:
    classes: dict[str, TableGenClass]

    def __init__(self):
        self.classes = dict()
        self.defs = dict()

    def addClass(self, name, record):
        self.classes[name] = record

    def getClasses(self):
        return self.classes

    def addDef(self, name, record):
        self.defs[name] = record

    def getValue(self, type_: TableGenType | binding.RecTy, value):
        if isinstance(type_, binding.RecTy):
            type_ = self.getType(type_.getAsString())

        if value.isConcrete():
            valueStr = value.getAsString()
            if valueStr == "?":
                return None
            if rec := self.defs.get(valueStr):
                return rec
            return type_(valueStr)
        else:
            if isinstance(value, binding.VarInit):
                return Var(value.getName())
            return value.getAsString()
            '''
            TODO: Implement Init Parsing
            if isinstance(value, binding.BinOpInit):
                value: binding.BinOpInit
                print("##x#>>", value.getAsString())
                lhs = value.getLHS()
                rhs = value.getRHS()
                print("###>>", lhs.getAsString())
                return BinOP(value.getOpcode(),
                             self.getValue(lhs.getType(), lhs),
                             self.getValue(rhs.getType(), rhs))
            '''

    def setField(self, rec: TableGenRecord, record: binding.Record):
        for value in record.getValues():
            valuename = value.getName()
            '''
            type_ = self.getType(value.getTypeName())
            # if value.
            value_ = self.getValue(type_, value.getValue())
            if value.isTemplateArg():
                rec.args[valuename] = (valuename, type_, value_)
            elif value.getName().startswith("__Arg_"):
                rec.defargs[valuename] = (valuename, type_, value_)
            else:
                rec.fields[valuename] = (valuename, type_, value_)
            '''

    def getType(self, typename):
        origin, *arg = typename.replace('>', '').split('<')
        match origin:
            case 'dag':
                return dag
            case 'int':
                return int
            case 'list':
                return list
            case 'string':
                return str
            case 'bit':
                return bit
            case 'bits':
                return bit
            case _:
                try:
                    return self.classes[typename]
                except KeyError:
                    raise ValueError(f"Unknown type: {typename}")

    def __dump__(self):
        recs = list(self.classes.values()) + list(self.defs.values())
        return "\n".join(map(lambda x: x.__dump__(), sorted(recs, key=lambda x: x.depth())))

    def __eq__(self, other):
        for kk, def_ in self.classes.items():
            ins1 = self.classes[kk]
            ins2 = other.classes[kk]
            if ins1.diff(ins2):
                return False

        for kk, def_ in self.defs.items():
            ins1 = self.defs[kk]
            ins2 = other.defs[kk]
            if ins1.diff(ins2):
                return False

        return True
import time
class TableGenLoader:

    def __init__(self):
        pass

    def load(self, filename, incdirs=None):
        s = time.time()
        incdirs = incdirs or list()
        Recs = binding.ParseTableGen(filename, incdirs)
        print("ParseTableGen", time.time() - s)
        return self.__load(Recs)

    def __load(self, Recs: binding.RecordKeeper):
        s = time.time()
        ctx = TableGenContext()
        for name, record in Recs.getClasses().items():
            ctx.addClass(name, TableGenClass(name))

        for name, record in Recs.getClasses().items():
            cls = ctx.classes[name]
            for superclass, _ in record.getSuperClasses():
                cls.superclasses.append(ctx.classes[superclass.getName()])
        print("Create Object", time.time() - s)

        s = time.time()
        for name, record in Recs.getDefs().items():
            superClses = \
                [ctx.classes[superclass.getName()] for superclass, _ in record.getSuperClasses()]
            ctx.addDef(name, TableGenRecord(name, superClses))

        print("Create Def", time.time() - s)
        s = time.time()

        for name, record in Recs.getClasses().items():
            ctx.setField(ctx.classes[name], record)

        print("Set Fields Class", time.time() - s)
        s = time.time()

        for name, record in Recs.getDefs().items():
            ctx.setField(ctx.defs[name], record)
        print("Set Fields Obj", time.time() - s)

        return ctx