import tablegen
import os

def test_1():
    root = os.path.dirname(__file__)
    ret = tablegen.ParseTableGen(f"{root}/A.td")
    assert(ret.getClass("myRecord").getName() == "myRecord")

    lst = ret.getAllDerivedDefinitions("myRecord")
    assert(tuple(rec.getName() for rec in lst) == ("rec1", "rec2"))

    lst = ret.getAllDerivedDefinitions("myRecord", "Inst")
    assert(lst[0].getName() == "rec2")

    anses = [
        ("int", "x"),
        ("int", "Z"),
        ("int", "a"),
        ("bit", "b"),
    ]
    for val, ans in zip(lst[0].getValues(), anses):
        assert((val.getTypeName(), val.getName()) == ans)

