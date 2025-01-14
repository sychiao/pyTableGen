import pytest
import tablegen.binding as binding
import os


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

def Init2Expr(v: binding.Init):
    if isinstance(v, binding.BinOpInit):
        return f"{v.getOpcode()}({Init2Expr(v.getLHS())}, {Init2Expr(v.getRHS())})"
    if isinstance(v, binding.VarInit):
        return f"Value('{v.getAsString()}')"
    if isinstance(v, binding.StringInit):
        return f"'{v.getAsString()}'"
    if isinstance(v, binding.IntInit):
        return v.getValue()
    return v.getAsString()+str(v)

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

def xA : A<12>;'''

    with open("t_testx.td", 'w') as f:
        f.write(content)
    Recs2 = binding.ParseTableGen(f't_testx.td')
    os.unlink('t_testx.td')

    print(">>CLASS: A")
    v = Recs2.getClass("A")
    for recVal in v.getValues():
        recName = '_'+recVal.getName().split(':')[1] if ':' in recVal.getName() else recVal.getName()
        print(f'''{recName} : {recVal.getType().getAsString()} = {Init2Expr(recVal.getValue())}''')
        print(">> recVal", recName, recVal.getType().getAsString(), Init2Expr(recVal.getValue()), recVal.isTemplateArg())
    print("------")

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

