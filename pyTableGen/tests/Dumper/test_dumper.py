import tablegen.dumper as dumper
from tablegen.unit.bits import Bits
import re

from tablegen.unit.record import TypedRecord
from tablegen.unit.bits import Bits
from dataclasses import dataclass, field
from tablegen.dumper import dumpTblRecord

from tablegen.context import TableGenContext
import tablegen.wrapper.recordkeeper as RK



class TextMatch:

    def __init__(self, pattern, *predicate):
        self.pattern = pattern
        self.predicates = predicate

    def __eq__(self, string):
        assert isinstance(string, str)
        return self.text_match(string, self.pattern, self.predicates)

    @staticmethod
    def text_match(ss, pattern, predicates = list()):
        if m := re.match(pattern, ss):
            return all(pred(m) for pred in predicates)
        return False

def test_dumpTbl():
    a = Bits('01011')
    Bits.b = Bits[4]()
    assert dumper.dumpTblValue(a) == TextMatch("{(.*)}", 
             lambda x: list(map(int, x.group(1).split(','))) == [0, 1, 0, 1, 1])
    # match Bits[4]() == {b{0}, b{1}, b{2}, b{3}}
    assert dumper.dumpTblValue(Bits.b) == TextMatch("{(.*)}", 
             lambda x: 
                x.group(1).replace(' ', '').split(',') == ['b{0}', 'b{1}', 'b{2}', 'b{3}'])

def test_dumpTblDecl():
    #a = Bits('01011')
    Bits.b = Bits[4]()
    #print(dumper.dumpTblDecl(a))
    print(dumper.dumpTblDecl(Bits.b))

def test_def():
    Bits.b = Bits[5]('01011')
    print(dumper.dumpTblDef(Bits.b))

@dataclass
class A(TypedRecord):
    x: int
    y: int

    def __post_init__(self):
        self.v = self.x + self.y

def test_Record():
    print(issubclass(A, TypedRecord))
    A.a = A(1, 2).let("a", 3)
    A.a.let("b", Bits[5]()).let("c", Bits[5]('01011')).let("d", A.a.b)
    print(A.a)
    print(">", dumper.dumpTblDef(A.a))

content = '''
class base1 {
   string name = "base1";
}
class base2<string _prefix> {
    string prefix = !strconcat(_prefix, "prefix");
}

defvar vv = {0,0,1,1};

def base : base1;

class A<int x, string v = "NAME"> : base1, base2<v> {
    defvar xaVal = 21;
    int a = 1;
    int value = !add(x, xaVal);
    base1 B = base;
    bits<2> rec;
    bits<4> XZ;
    bits<8> Inst;
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{3-2} = rec;
}

defvar yaVal = A<13>;

def xA : A<12>;'''

def test_context_dump():
    ctx = TableGenContext(RK.RecordKeeper.loads(content))
    rec = ctx.A(1, "123")
    rec.let("rd", Bits[8]()).let("Inst", rec.rd)
    print(rec.__def_dump__())
