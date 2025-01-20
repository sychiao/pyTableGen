from tablegen.unit.bits import Bits
import pytest
import tablegen.unit.bits

def test_0():
    if a := Bits.castfrom(1902):
        assert a.toint() == 1902
    
    a = Bits('01011')
    assert a.toint() == 11

    if a := Bits.castfrom(1902):
        assert a.toint() == 1902

    if a := Bits.castfrom([True, False, True]):
        assert a.toint() == 5

    with pytest.raises(TypeError):
        Bits[5.2]

    a = Bits('01011')
    assert isinstance(a, Bits)
    assert isinstance(a, Bits[5])
    assert isinstance(Bits.castfrom(1), Bits)
    assert not isinstance(Bits.castfrom(1024), Bits[5])


def test_1():
    a = Bits('01011')
    b = Bits('111')
    print(isinstance(a, Bits))
    #print(isinstance(1, Bits))
    print(isinstance(a, Bits[5]))

    if a := Bits.castfrom(1902):
        print(a.toint())
        print(a.bits)
        print(a[1:4])
        print(a[4:1])
        #a[1:4] = '1234'
        a[4:1] = 'xxxx'
        print("check 1", a)
        print("check 2", a[1:4])
        a[1:4] = b[0:1]
        print(a)

def test_2(): # test VarBits
    if a := Bits.castfrom(1902):
        assert a.toint() == 1902
        b = Bits[3]()
        print("TEST 1", a)
        a[1:4] = b[0:1]
        print("TEST 2",a)
        b[0] = 1
        print("CHECK", b[0])
        print("TEST 3",a)

def test_3():
    a = Bits([1, 0, 1, 1])
    assert a.toint() == 11
    a == Bits([1, 0, 1, 1])
    a != Bits([1, 0, 1, 0])
    a == Bits("1011")
    with pytest.raises(TypeError):
        a = Bits.castfrom(1.0123)

    with pytest.raises(ValueError):
        a == Bits[2]("101")