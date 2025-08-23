import pytest
import os

import tablegen.wrapper.recordkeeper as RK
from tablegen.unit.bits import Bits

def test_CacheDict():
    class TestCacheDict(RK.CacheDict):
        def __getf__(self, key):
            if key in [1, 2]:
                return key
            return None

    a = TestCacheDict()
    assert a.get(1) == 1
    assert a.get(1) == 1
    assert a.get(2) == 2
    assert a.get(2) == 2

    with pytest.raises(KeyError):
        a[3]

    d = RK.CacheDict()
    with pytest.raises(NotImplementedError):
        d[1]


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

def test_1():
    Recs = RK.RecordKeeper.loads(content)
    x = Recs.getRecord("xA")
    assert x
    assert x.a == 1
    assert x.value == 21 + 12
    assert x.B.name == "base1"
    # assert x.rec == 0
    assert x.XZ[0:2] == Bits([0, 1])
    # Note: the order of bits is reversed in the tablegen
    # XZ{3-2} = rec; => XZ[2:4] = rec;
    # because rec == rec{1-0} rather than rec{0-1}
    assert x.XZ[2:4] == x.rec
    assert x.XZ[4:2] != x.rec

def test_2():
    print("Wrapper test 2")
    Recs = RK.RecordKeeper.loads(content)
    for name, reccls in Recs.getClasses().items():
        print("class:", name, ":", reccls)
    
    for rec in Recs.getDefs():
        print("def:", rec)
        for key, valu in rec.items.items():
            if isinstance(valu, RK.TableGenRecord):
                print(f"    {key}: {valu.defname} ({type(valu)}, {valu.classes})")
            else:
                print(f"    {key}: {valu} ({type(valu)})")
