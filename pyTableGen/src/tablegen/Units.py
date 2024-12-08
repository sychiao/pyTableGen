import tablegen.binding as binding
from typing import Type
import copy

TableGenType = Type['dag'] | Type[int] | Type[list] | Type['TableGenClass']  | Type[str]
class dag:
    def __init__(self, v):
        pass

class bit:
    def __init__(self, v):
        self.v = v

    def __eq__(self, other):
        return self.v == other.v

    def __repr__(self) :
        return str(self.v)

class BinOP:
    def __init__(self, BINOP, LHS, RHS):
        self.BINOP = BINOP
        self.LHS = LHS
        self.RHS = RHS

    def op(self):
        match self.BINOP:
            case binding.BinaryOp.ADD: return f"!add"

    def __repr__(self):
        return f"{self.op()}({self.LHS}, {self.RHS})"

class Var:

    def __init__(self, valuename):
        self.valuename = valuename

    def __repr__(self):
        return self.valuename.split(':')[1]

    def __eq__(self, other):
        if not isinstance(other, Var):
            return False
        return self.valuename == other.valuename

    def __call__(self, **kwds):
        _, v = self.valuename.split(':')
        return kwds[v]

def getQuotedName(value):
    return f'"{value}"'.replace('""', '"')

def dumpType(type_):
    if type_ == dag:
        return "dag"
    elif type_ == int:
        return "int"
    elif type_ == list:
        return "list"
    elif type_ == str:
        return "string"
    elif type_ == bit:
        return "bit"
    else:
        return type_.name

class TableGenField: # RecordVal
    name: str
    type:  TableGenType
    value: str

    def __init__(self, name, type, value):
        self.name = name
        self.type = type
        self.value = value

    def __eq__(self, other):
        return self.name == other.name and self.type == other.type and self.value == other.value

class TableGenSimpleRecord:
    '''
    SimpleRecord - is record with less one direct superclasses
    '''
    pass

def LazyAttr(func):
    def wrapper(self):
        try:
            return getattr(self, '__lazy_'+func.__name__)
        except AttributeError:
            value = func(self)
            setattr(self, '__lazy_'+func.__name__, value)
            return value
    return wrapper


class TableGenRecord: # def Record
    name: str | None
    superclasses: list['TableGenClass']
    fields: dict[str, 'TableGenField']

    def __init__(self, name=None, superclasses=None, args=None, fields=None):
        self.name = name
        self.superclasses = superclasses or list()
        self.args = args or dict()
        self.fields = fields or dict()
        self.defargs = dict()

    @LazyAttr
    def depth(self):
        if not self.superclasses:
            return 0
        return 1 + max(cls.depth() for cls in self.superclasses)

    @LazyAttr
    def getDirectClasses(self):
        supercls = set()
        directSCs = list()
        for cls in reversed(self.superclasses):
            if cls in supercls:
                continue
            supercls.add(cls)
            for sscls in cls.superclasses:
                supercls.add(sscls)
            # print("supercls:", [cls.name for cls in supercls])
            directSCs.append(cls)
        return directSCs

    def getDefArgs(self):
        defargs = dict()
        for cls in self.getDirectClasses():
            if cls.args:
                defargs[cls.name] = {argname.replace(f"{cls.name}:", ""): None for argname in cls.args}
                for _, arg in self.defargs.items():
                    if arg.name.startswith('__Arg_'):
                        Clsname, ArgName = arg.name.replace("__Arg_", "").split("_", maxsplit=1)
                        if Clsname == cls.name:
                            defargs[cls.name][ArgName] = arg.value
                        if f"__Args_{Clsname}" == cls.name:
                            defargs[cls.name][ArgName] = arg.value
        return defargs

    def isDirectClass(self, cls):
        return cls in self.getDirectClasses()

    def getAllInheritRecords(self):
        inheritRecords = list()
        if self.getDirectClasses():
            for cls in self.getDirectClasses():
                if cls.args:
                    inheritRecords.append(cls(*self.getDefArgs()[cls.name].values()))
                else:
                    inheritRecords.append(cls())
        return inheritRecords

    def getinheritRecord(self):
        rr = TableGenRecord(None, {}, {}, {})
        for rec in self.getAllInheritRecords():
            rr = rec.union(rr)
        return rr

    def __xor__(self, other):
        return self.diff(other)

    def __or__(self, other):
        return self.union(other)

    def __sub__(self, other):
        return self.sub(other)

    def union(self, other):
        return TableGenRecord(self.name,
                              self.superclasses + other.superclasses,
                              {**self.args, **other.args},
                              {**self.fields, **other.fields})

    def sub(self, other):
        return {k: v for k, v in self.fields.items() if k not in other.fields}

    def diff(self, other):
        #for k, v in self.fields.items():
        #    if k in other.fields and other.fields[k].value != v.value:
        #        print(f"diff: {k} {v.value}({type(v.value)}) {other.fields[k].value}({type(other.fields[k].value)})")
        return {k: v for k, v in self.fields.items() if k in other.fields and other.fields[k].value != v.value}

    def dumpTitle(self):
        return f"def {' ' if self.name.startswith("anonymous") else self.name}"

    def dumpSuperClasses(self):
        s = ""
        if self.getDirectClasses():
            lst = list()
            for cls in reversed(self.getDirectClasses()):
                if cls.args:
                    lst.append(f'''{cls.name}<{", ".join(f"{v if v else '?'}" for k, v in self.getDefArgs()[cls.name].items())}>''')
                else:
                    lst.append(cls.name)
            s += f" : {', '.join(lst)}"
        return s

    def dumpAdditioDefs(self):
        addition = list()
        for _, f in self.diff(self.getinheritRecord()).items():
            addition.append(f"  let {f.name} = {f.value};")
        for _, f in self.sub(self.getinheritRecord()).items():
            addition.append(f"  {dumpType(f.type)} {f.name} = {f.value};")
        return addition

    def __dump__(self):
        '''
        Dump use to recover the original tablegen record
        however, tablegen will not store the original argument,
        so when define the tablegen record,
        you should add additoinal fields which start with __Arg_ to store the original argument
        if we cannot recover the original argument, we will use '?' to replace it
        and set the value of field directly.

        e.g.
        def Inst : Inst<"ADD"> {
            string __Arg_Inst = "ADD"; // recoverable
        }

        def Inst : Inst<"ADD">; // cannot recoverable
        dump maybe:
        def Inst : Inst<?> {
            let Name = "ADD";
        }
        '''
        s = self.dumpTitle()
        s += self.dumpSuperClasses()
        if addition := self.dumpAdditioDefs():
            s += " {\n" + "\n".join(addition) + "\n}"
        else:
            s += ";"
        return s

    def __repr__(self):
        s = f"@{self.name} : {', '.join(cls.name for cls in self.getDirectClasses())}\n"
        s += f"Superclasses:{' | '.join(cls.name for cls in self.superclasses)}\n"
        s += f"getDefArgs: {self.getDefArgs()}\n"
        if self.args:
            s += "Args:\n"
            s += f" {'\n'.join(f'  {arg.name}: {arg.value}' for arg in self.args.values())}\n"
        if self.defargs:
            s += "DefArgs:\n"
            s += f"{'\n'.join(f'  {arg.name}: {arg.value}' for arg in self.defargs.values())}\n"
        if self.fields:
            s += "Fields:\n"
            s += f"{'\n'.join(f'  {dumpType(field.type)} {field.name}= {field.value}' for field in self.fields.values())}\n"
        return s

class TableGenClass(TableGenRecord): # class Record

    def __call__(self, *args, **kwds):
        posarg = list(args) + [None] * (len(self.args) - len(args))
        dct = {k.replace(self.name+":", ""): (getQuotedName(v) if isinstance(v, str) else v) for k, v in zip(self.args, posarg)}
        dct.update({k: (getQuotedName(v) if isinstance(v, str) else v) for k, v in kwds.items()})
        fields = copy.copy(self.fields)
        for name, field in self.fields.items():
            if isinstance(field.value, Var):
                fields[name] = TableGenField(name, field.type, field.value(**dct))
        return TableGenRecord(None, [self] + self.superclasses, {}, fields)

    def dumpTitle(self):
        s = f"class {self.name}"
        if self.args:
            args = \
                [f"{dumpType(arg.type)} {arg.name.replace(f"{self.name}:", "")}" for arg in self.args.values()]
            s += f"<{', '.join(args)}>"
        return s

    def dumpAdditioDefs(self):
        if self.name.startswith("__Args_"):
            return [f"  {dumpType(f.type)} {f.name} = {f.value};" for f in self.defargs.values()]
        return super().dumpAdditioDefs()