import pytest
from tablegen.unit.dag import DAG, Node
import tablegen.RecordKeeper as RK

def test_0():
    a = DAG('ADD', 'a', 'b')
    b = DAG('NEW', 'a', 'b', 'c')
    c = DAG('CON', RD=1, RS=2)

    def matcher(a: DAG):
        match a:
            case ('ADD', x, y):
                assert x == 'a'
                assert y == 'b'
            case  ('NEW', x, y, z):
                assert x == 'a'
                assert y == 'b'
                assert z == 'c'
            case  ('CON', *args):
                assert args == (1, 2)
    matcher(a)
    matcher(b)
    assert c['RD'] == 1

    with pytest.raises(TypeError):
        c['RD'] = '1' # type: ignore

content = '''
class base1 {
   string name = "base1";
}
class base2<string _prefix> {
    string prefix = !strconcat(_prefix, "prefix");
}

defvar vv = {0,0,1,1};

def base : base1;

class A<dag _pat> : base1, base2<"name"> {
    dag pat = _pat;
}

def xA : A<(base 1:$a, 2:$b)>;'''

def test_1():
    Recs = RK.RecordKeeper.loads(content)
    x = Recs.getRecord("xA")
    match x.pat:
        case ('base', Node('b', a), b):
            assert a == 100 # will not match this because name
        case ('base', Node('a', a), b):
            assert a == 1
            assert b == 2
