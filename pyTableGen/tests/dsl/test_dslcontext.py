import tablegen.wrapper.recordkeeper as RK
from tablegen.unit.bits import Bits
from tablegen.dsl.record import RecType, TDRecord, UnionTDRecord, TblRecMetaData, PyRecord
from tablegen.dsl.context import RecordContext
from tablegen.dsl.dumper import dumpDef
import sys

content = '''
class base1 {
   string name = "base1";
}
class base2<string _prefix> {
    string prefix = !strconcat(_prefix, "prefix");
}
class base3 {
  int value = 123;
}

defvar vv = {0,0,1,1};

def emptry {
  int value = 1;
}

def base : base1, base3;

class A<int x, string v = "NAME"> : base1, base2<v> {
    defvar xaVal = 21;
    int a = 1;
    int value = !add(x, xaVal);
    base1 B = base;
    dag d = (base 1:$rd, 2:$rs2, 3:$rs1);
    bits<2> rec;
    bits<4> XZ;
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{3-2} = rec;
}

defvar yaVal = A<13>;

def xA : A<12>;

class BUGCLASS {
  BUGCLASS self = !cast<BUGCLASS>(NAME);
}

def BUGDEF : BUGCLASS;
'''

def test_RK():
    print("Wrapper test 2")
    Recs = RK.RecordKeeper.loads(content)
    ctx = RecordContext.load(Recs)

    for name, value in ctx.__dict__.items():
        if isinstance(value, RecType):
            print(f"class ctx.{name}", "==\n", value)
            print("\t>", value.__mro__)
            print("\t>", value.tbl.fields, id(value.tbl))
        else:
            print(f"def ctx.{name}", "==\n", value)

    class A(PyRecord, TDRecord=ctx.A):

        def __init__(self, x: int, v: str = "NAME"):
            self.xaVal = 21
            self.a = 1

    ta = ctx.A(1, "123")
    a = A(1, "123")
    print(ctx.base1.tbl.signature)
    ctx.obj = ctx.base1()
    print(a)
    print(isinstance(a, ctx.A))
    a.value = 12
    a.new_val = ctx.obj
    print(ctx.obj.tbl.file)
    ctx.dump(sys.stdout, [a])
    print(ctx.obj.tbl.file)
    print(ctx.xA.tbl.file)
