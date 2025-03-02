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
    assert a == Bits([1, 0, 1, 1])
    assert a != Bits([1, 0, 1, 0])
    assert a == Bits("1011")
    with pytest.raises(TypeError):
        a = Bits.castfrom(1.0123)

    with pytest.raises(ValueError):
        z = Bits[2]("101")

def test_kind_of_bits():
    prefix = Bits('00')
    funct5 = Bits('10111')
    rd = Bits[8]().bind('rd')
    rs1 = Bits[5]().bind('rs1')
    rs2 = Bits[5]().bind('rs2')
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

def test_kind_of_bits2():
    prefix = Bits('00')
    funct5 = Bits('10111')
    Bits.rd = Bits[8]()
    Bits.rs1 = Bits[5]()
    Bits.rs2 = Bits[5]()
    funct3 = Bits('000')
    opcode = Bits('0110011')
    Enc = Bits([*prefix, *funct5, *Bits.rd[3:8], *Bits.rs1, *funct3, *Bits.rs2, *opcode]) # type: ignore

    assert Bits.rs1.isVar()  # type: ignore
    assert prefix.isConstant()
    assert not Enc.isVar() and not Enc.isConstant()
    ret = Bits()
    for v in Enc.fragments().values():
        ret = ret @ v
        assert v.isVar() or v.isConstant()
    assert ret == Enc

def test_operator_of_bits():
    a = Bits.castfrom(1)
    b = Bits.castfrom(2)
    c = Bits.castfrom(3)
    if a is not None and \
       b is not None and \
       c is not None:
        assert a + b == Bits.castfrom(3)
        assert a + c == Bits('100')

    x = Bits('101')
    y = Bits('010')
    assert x @ y == Bits('101010')
