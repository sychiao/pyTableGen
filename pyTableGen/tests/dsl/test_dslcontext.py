import tablegen.wrapper.recordkeeper as RK
from tablegen.unit.bits import Bits
from tablegen.dsl.record import TDRecord, UnionTDRecord, TblRecMetaData
from tablegen.dsl.context import TBLParser

content = '''
class base1 {
   string name = "base1";
}
class base2<string _prefix> {
    string prefix = !strconcat(_prefix, "prefix");
}
class base3;

defvar vv = {0,0,1,1};

def base : base1, base3;

class A<int x, string v = "NAME"> : base1, base2<v> {
    defvar xaVal = 21;
    int a = 1;
    int value = !add(x, xaVal);
    base1 B = base;
    bits<2> rec;
    bits<4> XZ;
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{3-2} = rec;
}

defvar yaVal = A<13>;

def xA : A<12>;'''

def test_RK():
    print("Wrapper test 2")
    TDRecMap = dict()
    Recs = RK.RecordKeeper.loads(content)
    parser = TBLParser(Recs)
    for name, reccls in Recs.getClasses().items():
        parser.getTDRecordType(reccls)

    print("----- Classes -----")
    for k, v in parser.TDRecordTypeMapping.items():
        print(f">> {v.__name__} {v.__mro__})")

    print('----- Definitions -----')
    lst = list()
    for rec in Recs.getDefs():
        rr = parser.getTDRecord(rec)
        lst.append(rr)

    for rr in lst:
        print(rr)