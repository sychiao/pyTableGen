from tablegen.dsl.bits import Bits, VarBit
import pytest

def test_0():
    print("==== TEST BITS 0 ===")
    if a := Bits(bin(1902)[2:]):
        assert a.toint() == 1902
    
    a = Bits('01011')
    assert a.toint() == 11

    with pytest.raises(TypeError):
        Bits[5.2]

    a = Bits('01011')
    assert isinstance(a, Bits)
    assert isinstance(a, Bits[5])

def test_1():
    print("==== TEST BITS 1 ===")
    a = Bits('01011')
    b = Bits('111')
    assert isinstance(a, Bits)
    assert isinstance(a, Bits[5])

    if a := Bits(bin(1902)[2:]):
        print(a.toint())
        print(a.bits)
        assert a[4:1].bits == tuple(reversed(a[1:4].bits))
        a[4:1] = 'xxxx'
        print("check 1", a)
        print("check 2", a[1:4])

def test_2(): # test VarBits
    print("==== TEST BITS 2 ===")
    if a := Bits(bin(1902)[2:]):
        assert a.toint() == 1902
        b = Bits[4]()
        print("TEST 1", a)
        a[1:4] = b
        print("TEST 2",a)
        b[0] = 1
        print("CHECK", b[0])
        print("TEST 3",a)

def test_3():
    a = Bits([1, 0, 1, 1])
    assert a.toint() == 11
    assert a == Bits([1, 0, 1, 1])
    assert a != Bits([1, 0, 1, 0])
    assert a == Bits("1011")
    with pytest.raises(ValueError):
        z = Bits[2]("101")

def test_kind_of_bits():
    prefix = Bits('00')
    funct5 = Bits('10111')
    rd = Bits[8]('rd')
    rs1 = Bits[5]('rs1')
    rs2 = Bits[5]('rs2')
    funct3 = Bits('000')
    opcode = Bits('0110011')
    Enc = Bits([*prefix, *funct5, *rd[3:8], *rs1, *funct3, *rs2, *opcode])

    assert rs1.isVar()
    assert prefix.isConstant()
    assert not Enc.isVar() and not Enc.isConstant()
    ret = Bits()
    for v in Enc.fragments().values():
        ret = ret @ v
        assert v.isVar() or v.isConstant()
    assert ret == Enc