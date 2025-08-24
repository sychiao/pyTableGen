from tablegen.unit.value import Unset, UnknownValue

def test_unset():
    a = Unset(int)
    b = Unset(int)
    c = Unset(str)
    assert a is b
    assert a is not c
    assert str(a) == "?"
    assert repr(a) == "Unset(<class 'int'>)"

def test_unknown():
    a = UnknownValue(int)
    b = UnknownValue(int)
    c = UnknownValue(str)
    assert a is b
    assert a is not c
    assert isinstance(a, UnknownValue)
    assert str(a) == "Unk"
    assert repr(a) == "UnknownValue(<class 'int'>)"