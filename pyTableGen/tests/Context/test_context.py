from tablegen.context import TableGenContext
from tablegen.unit.record import TableGenRecord, TypedRecord
from dataclasses import dataclass
import pytest
import tablegen.wrapper.recordkeeper as RK

@dataclass
class A(TypedRecord):
    x: int
    y: int

def test_1():
    ctx = TableGenContext()

    ctx.addDef(A(1, 2), "a")
    ctx.addDef(A(3, 4), "b")
    ctx.addDef(A(5, 6))

    ctx.c = A(1, 2)

    if v:= ctx.getRecord("a"):
        v.cast(A).x = 5
    if x := ctx.getRecord("a"):
        assert x.cast(A).x == 5
    
    # Note we can combined cast and check None in one line
    if v:= ctx.getRecord[A]("a"):
        v.x = 5
    if x := ctx.getRecord("a"):
        assert x.cast(A).x == 5
    
    # Note we can combined cast and check None in one line
    if v:= ctx.get[A]("a"):
        v.x = 5
    if x := ctx.get("a"):
        assert x.cast(A).x == 5

    assert ctx.get("d", None) == None
    assert ctx.get[A]("d", None) == None
    assert ctx.get("a") == ctx.a
    with pytest.raises(AttributeError):
        ctx.d

    with pytest.raises(ValueError):
        ctx.addDef(A(1, 2), "a")

    assert isinstance(A(1, 2), TableGenRecord)
    #with pytest.raises(ValueError):
    #    ctx.a = A(1, 2)

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
    let XZ{0} = 0;
    let XZ{1} = 1;
    let XZ{3-2} = rec;
}

defvar yaVal = A<13>;

def xA : A<12>;'''


def test_2():
    Recs = RK.RecordKeeper.loads(content)
    ctx = TableGenContext(Recs)
    if x := ctx.getRecord("xA"):
        assert x.parent == ctx
        assert x.a == 1

    if rk := ctx.getRecordKeeper():
        if lsta := rk.getDefs("A"):
            assert len(list(lsta)) == 2

    if rk := ctx.getRecordKeeper():
        if lsta := rk.getDefs(A):
            assert len(list(lsta)) == 2
    
    v = ctx.A(12, "123").let("MMO", 1)
    print(ctx.A)
    print("A Obj", v.__dump__())
    print(v.additional_fields())
    print(v.__reset_field__)