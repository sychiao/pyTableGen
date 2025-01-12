import pytest
import os

import tablegen.RecordKeeper as RK

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

def test_1():
    with open("t_test.td", 'w') as f:
        f.write(content)
    Recs = RK.load(f't_test.td')
    os.unlink('t_test.td')

    x = Recs.getRecord("xA")
    print(x)