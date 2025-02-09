import pytest
import tablegen.binding as binding
import os

from tablegen.unit.bits import Bits


'''
class A<int x, string v = "NAME"> : base1, base2<v> {
    defvar xaVal = 21;
    int a = 1;
    int value = !add(x, xaVal);
    base1 B = base;
    bits<2> rec;
    bits<4> XZ;
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{2-3} = rec;
}

==> Python Wrapper

@dataclass
class A(TableGenRecord, record=RecA):
    x: int
    v: str = "NAME"
    xaVal: int = field(init=False)
    a: int = field(init=False)
    value: int = field(init=False)
    B: base1 = field(init=False)
    rec: Bits[2] = field(init=False)
    XZ: Bits[4] = field(init=False)
    XZ0: int = field(init=False)
    XZ1: int = field(init=False)
    XZ2: Bits[2] = field(init=False)

    AttributeSetter({
        "xaVal": 21,
        "a": 1,
        "value": Add(Getter('x'), Getter('xaVal')),
        "B": Value(self.ctx, 'base'),
        "rec": Bits[2],
        "XZ": Bits[4],
        "XZ0": 0,
        "XZ1": 1,
        "XZ2": Getter('rec')
    })

    def __post_init__(self):
        self.xaVal = 21
        self.a = 1
        self.value = add(self.x, self.xaVal)
        self.B = base
        self.rec = Bits[2]()
        self.XZ = Bits[4]()
        self.XZ0 = 0
        self.XZ1 = 1
        self.XZ2 = self.rec
'''

def dumpInit(v: binding.Init):
    if isinstance(v, binding.BinOpInit):
        return f"{v.getOpcode()}({dumpInit(v.getLHS())}, {dumpInit(v.getRHS())})"
    elif isinstance(v, binding.VarInit):
        return f"self.{v.getAsString().split(':')[1]}"
    elif isinstance(v, binding.StringInit):
        return f"'{v.getAsString()}'"
    elif isinstance(v, binding.IntInit):
        return v.getValue()
    elif isinstance(v, binding.BitsInit):
        numbits = v.getNumBits()
        bitsstr = ", ".join([v.getBit(idx).getAsString() for idx in range(numbits)])
        return f"Bits[{numbits}]({bitsstr})"
    return v.getAsString()+str(v)

def Init2Expr(v: binding.Init):
    if isinstance(v, binding.BinOpInit):
        return f"{v.getOpcode()}({Init2Expr(v.getLHS())}, {Init2Expr(v.getRHS())})"
    if isinstance(v, binding.VarInit):
        return f"self.{v.getAsString()}"
    if isinstance(v, binding.StringInit):
        return f"'{v.getAsString()}'"
    if isinstance(v, binding.IntInit):
        return v.getValue()
    return v.getAsString()+str(v)

def Binding2Type(v: binding.RecTy):
    if isinstance(v, binding.BitsRecTy):
        print("DEBUG", v.getNumBits())
        return Bits[v.getNumBits()]
    elif isinstance(v, binding.StringRecTy):
        return str
    elif isinstance(v, binding.IntRecTy):
        return int
    elif isinstance(v, binding.ListRecTy):
        return list
    elif isinstance(v, binding.DagRecTy):
        return dict
    elif isinstance(v, binding.RecordRecTy):
        pass
    print("Warning: Binding2Type unhandle type", v)
    return v.getAsString()

from dataclasses import dataclass, field, is_dataclass, make_dataclass, fields
import inspect

class TableGenClass:

    def __dump__(self):
        args = list()
        args_name = list()
        if is_dataclass(self):
            for f in fields(self):
                if f.init:
                    args.append(f"{getattr(self, f.name)}")
                    args_name.append(f"{f.name}")
            return f"{type(self).__name__}<{', '.join(args)}>  /*args: {' '.join(args_name)}*/"
        else:
            raise ValueError("TableGenClass must be a dataclass")
    

def Record2TableGenClass(rec: binding.Record):
    fields = []
    print(f'''class {rec.getName()} {{''')
    for recVal in rec.getValues():
        recName = recVal.getName().split(':')[1] if ':' in recVal.getName() else recVal.getName()
        if recVal.isTemplateArg():
            print(f'''\t {recName}(Args) = {dumpInit(recVal.getValue())};''')
            fields.append((recName, Binding2Type(recVal.getType())))
        else:
            print(f'''\t {recName} = {dumpInit(recVal.getValue())};''')
            fields.append((recName, Binding2Type(recVal.getType()), field(init=False)))
    print("}")
    return make_dataclass(rec.getName(), fields, bases=(TableGenClass,))

def test_1():
    content = '''
class base1;
class base2<string _prefix> {
    string prefix = !strconcat(_prefix, "prefix");
}

def base : base1;

class A<int x, string v = "NAME"> : base1, base2<v> {
    defvar xaVal = 21;
    int a = 1;
    int value = !add(x, xaVal);
    base1 B = base;
    bits<2> rec;
    bits<4> XZ;
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{2-3} = rec;
}

defvar yaVal = A<13>;
def xB : A<12>;
def xA : A<12> {let rec={1,1};}'''

    with open("t_testx.td", 'w') as f:
        f.write(content)
    Recs2 = binding.ParseTableGen(f't_testx.td')
    os.unlink('t_testx.td')

    print(Recs2.getDef("xA").getValue("XZ").getValue().getAsString())
    print(Recs2.getDef("xB").getValue("XZ").getValue().getAsString())

    print(">>CLASS: A")
    v = Recs2.getClass("A")
    RecA = Record2TableGenClass(v)
    print("------")
    print("MAKE:", RecA, inspect.get_annotations(RecA.__init__))
    print(RecA(2, "name").__dump__())

    v = Recs2.getClass("A").getValue("value").getValue()
    print(v)

    vkz = Recs2.getClass("A").getValue("prefix").getValue()
    print("prefix", vkz)

    k = Recs2.getClass("A").getValue("B").getValue()
    print("k", k)

    ll = Recs2.getClass("A").getValue("XZ").getValue()
    print("NumBits: ", ll.getNumBits())
    print("ll", ll, ll.getAsString())
    for i in range(ll.getNumBits()):
        print("BITS:", ll.getBit(i), ll.getBit(i).getAsString())
        if isinstance(ll.getBit(i), binding.VarBitInit):
            print(ll.getBit(i).getBitVar().getAsString())

    # Bits a[2-3] = x[1-2]

    if isinstance(v, binding.BinOpInit):
        print(v.getOpcode())
        print(v.getLHS().getAsString(), v.getLHS())
        print(v.getRHS().getAsString(), v.getRHS())

test_1()

