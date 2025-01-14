from tablegen.unit.bits import Bits
import pytest
import tablegen.unit.bits

def test_0():
    if a := Bits.castfrom(1902):
        assert a.toint() == 1902
    
    a = Bits('01011')
    assert a.toint() == 11

    if a := Bits.castfrom(bin(1902)):
        assert a.toint() == 1902

    if a := Bits.castfrom([True, False, True]):
        assert a.toint() == 5

    with pytest.raises(TypeError):
        Bits[5.2]

    a = Bits('01011')
    assert isinstance(a, Bits)
    assert isinstance(a, Bits[5])
    assert isinstance(1, Bits)
    assert not isinstance(1024, Bits[5])


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