import tablegen.binding as binding
import os

def test_1():
    content = '''
class base1;
class base2;
class A : base1, base2 {
    int a = 1;
    bits<4> b = 13;
}

def xA : A;

class B {
    int a = 1;
    bits<4> b = 12;
    bit c = 1;
    string name = "123";
    list<int> x = [1, 2, 3];
    dag y =(xA 1, 2, 3);
    A z;
}

def xB : A, B;
'''
    with open("_test.td", 'w') as f:
        f.write(content)
    Recs2 = binding.ParseTableGen(f'_test.td')
    x = Recs2.getClass('A').getValue('a').getValue()
    w = Recs2.getClass('A').getValue('b').getValue()

    assert Recs2.getClass('B').getValue('a').getType().getRecTyKind() == binding.RecTyKind.IntRecTyKind
    assert Recs2.getClass('B').getValue('b').getType().getRecTyKind() == binding.RecTyKind.BitsRecTyKind
    assert Recs2.getClass('B').getValue('c').getType().getRecTyKind() == binding.RecTyKind.BitRecTyKind
    assert Recs2.getClass('B').getValue('x').getType().getRecTyKind() == binding.RecTyKind.ListRecTyKind
    assert Recs2.getClass('B').getValue('y').getType().getRecTyKind() == binding.RecTyKind.DagRecTyKind
    assert Recs2.getClass('B').getValue('z').getType().getRecTyKind() == binding.RecTyKind.RecordRecTyKind

    BaT = Recs2.getClass('B').getValue('a').getType()
    AaT = Recs2.getClass('A').getValue('a').getType()
    assert id(AaT) == id(BaT)
    nametype = Recs2.getClass('B').getValue('name').getType()
    assert nametype.getAsString() == "string"

    bitrec = Recs2.getClass('B').getValue('b').getValue().getType()
    assert isinstance(bitrec, binding.BitsRecTy)
    assert bitrec.getAsString() == 'bits<4>'

    recordty = Recs2.getClass('B').getValue('z').getType()
    assert isinstance(recordty, binding.RecordRecTy)
    print(recordty.getAsString())

    assert [r.getName() for r in recordty.getClasses()] == ['A']
    assert [r.getName() for r in Recs2.getDef("xB").getType().getClasses()] == ['A', 'B']


    