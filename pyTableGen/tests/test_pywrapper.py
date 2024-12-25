from tablegen.unit.record import TableGenRecord
from tablegen.context import TableGenContext

import tablegen.binding as binding
import os
import time

class A(TableGenRecord):
    pass

class X(TableGenRecord):
    pass

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
    A z = A<>;
}

def xB : A, B;

class C {
  B val = xB;
}

def xC : C;

'''
    with open("t_test.td", 'w') as f:
        f.write(content)
    Recs2 = binding.ParseTableGen(f't_test.td')
    os.unlink('t_test.td')

    xBRec = Recs2.getDef('xB')
    ctx = TableGenContext()
    z = TableGenRecord(xBRec, ctx)
    print(z, isinstance(z, A), isinstance(z, X))
    print("a", z.a)
    print(z.b)
    print("c", z.c)
    print("name:", z.name)
    print("x", z.x)
    print("y", z.y)
    print("z", z.z)

    class Empty:
        pass

    s = time.time()
    x = Empty()
    e = time.time()
    print("create object Empty Object", e - s)

    
    rr = Recs2.getDef('xC')
    s = time.time()
    CIns = TableGenRecord(rr, ctx)
    e = time.time()
    print("create object wrapper need", e - s)

    s = time.time()
    CIns2 = TableGenRecord(rr, ctx)
    e = time.time()
    print("create cached wrapper need", e - s)

    s = time.time()
    print(CIns.val)
    e = time.time()
    print("create object need", e - s)

test_1()