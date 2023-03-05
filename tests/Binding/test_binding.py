import tablegen.binding
import os

def test_1():
    root = os.path.dirname(__file__)
    ret = tablegen.binding.ParseTableGen(f"{root}/A.td")
    assert(ret.getClass("myRecord").getName() == "myRecord")

    for k, v in ret.getClasses().items():
        assert(k == v.getName())

    lst = ret.getAllDerivedDefinitions("myRecord")
    assert(tuple(rec.getName() for rec in lst) == ("rec1", "rec2"))

    lst = ret.getAllDerivedDefinitions("myRecord", "Inst")
    assert(lst[0].getName() == "rec2")

    anses = [
        ("int", "x"),
        ('string', '_name'),
        ("int", "Z"),
        ('list<int>', 'lst'),
        ("int", "a"),
        ("bit", "b"),
    ]
    for val, ans in zip(lst[0].getValues(), anses):
        assert((val.getTypeName(), val.getName()) == ans)

def test_2():
    root = os.path.dirname(__file__)
    ret = tablegen.binding.ParseTableGen(f"{root}/A.td")
    rec = ret.getClass("myRecord")
    # for loc in rec.getLoc():
    #     print(">", loc.getPointer())
    # for loc in rec.getForwardDeclarationLocs():
    #     print(">", loc.getPointer())
    NameInit = rec.getNameInit()
    assert(NameInit.getValue() == "myRecord")
    assert(NameInit.getAsString() =='''"myRecord"''')
    assert(NameInit.isConcrete() == True)
    assert(NameInit.getFormat() == tablegen.binding.StringFormat.SF_String)

def test_3():
    print("Dump log Test_3\n")
    root = os.path.dirname(__file__)
    ret = tablegen.binding.ParseTableGen(f"{root}/A.td")
    rec = ret.getClass("Inst")
    assert(rec.isClass)
    print("RecT", rec.getType().getRecTyKind())
    assert(rec.getType().getClasses()[0].getName() == "Base")
    for recT in rec.getType().getClasses():
        print(recT.getName())


    defInit = rec.getDefInit()
    assert(defInit.getAsString() == "Inst")
    assert(defInit.getDef().getName() == "Inst")

    for value in rec.getValues():
        print(value.getTypeName(), value.getName(), f"=({value.getValue().getKind()})" , value.getValue().getAsString())

def test_4():
    print("Dump log Test_4\n")
    root = os.path.dirname(__file__)
    ret = tablegen.binding.ParseTableGen(f"{root}/A.td")
    rec = ret.getClass("Template")
    
    for targs in rec.getTemplateArgs():
        print(targs, targs.getAsString(), targs.getKind(), rec.isTemplateArg(targs))
    print(">")
    for value in rec.getValues():
        print(value.getTypeName(), value.getName(), f"=({value.getValue().getKind()})" , value.getValue().getAsString())
        print(rec.getValue(value.getName()), value)
    assert(rec.isValueUnset("xx"))

def test_5():
    print("Dump log Test_5\n")
    root = os.path.dirname(__file__)
    ret = tablegen.binding.ParseTableGen(f"{root}/A.td")
    rec = ret.getDef("XX")
    
    for value in rec.getValues():
        print(value.getTypeName(), f"Name:{value.getName()}", f"=({value.getValue().getKind()})" , value.getValue().getAsString())
        print(value.getValue().getOperator().getAsString())
        for args in value.getValue().getArgs():
            print(args.getValue())

        print(value.getValue().getNumArgs())
        print(value.getValue().getArg(0))

        #for i in range(value.getValue().arg_size()):
        #    print(value.getValue().getArg(i))