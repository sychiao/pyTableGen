import re
from ._base import TableGenType, Unset
class VarBit(TableGenType):

    def __init__(self, Owner, index):
        self.Owner = Owner
        self.index = index
    
    def value(self):
        return self.Owner[self.index]
    
    def __eq__(self, other):
        selfname = self.Owner.name
        othername = other.Owner.name
        print("__eq__", selfname, othername)
        if selfname == othername:
            print(self.index , other.index)
            return self.index == other.index
        return False

    def __repr__(self):
        if isinstance(self.value(), VarBit):
            if isinstance(self.Owner, Bits):
                return f'{self.Owner.defname}[{self.index}]'
            return f'{self.Owner}[{self.index}]'
        else:
            return f'{self.value()}'

class Bits(TableGenType):
    Length = -1
    bits: tuple
    __cache__ = dict()

    def __init__(self, bits = None):
        if bits:
            def toBit(bit, idx):
                if isinstance(bit, VarBit):
                    return bit
                elif not bit or bit == '0':
                    return '0'
                elif isinstance(bit, Unset):
                    return VarBit(self, idx)
                else:
                    return '1'
            self.bits = tuple([toBit(bit, idx) for idx, bit in enumerate(bits)])
            if self.Length > 0:
                if len(self.bits) != self.Length:
                    raise ValueError(f"Bits[{self.Length}] must have {self.Length} bits, not {len(bits)}")
            else:
                self.Length = len(bits)
        else:
            self.bits = tuple([VarBit(self, i) for i in range(self.Length)])

    def __class_getitem__(cls, item):
        if isinstance(item, int):
            if cs := Bits.__cache__.get(item):
                return cs
            else:
                type_name = f'{cls.__name__}[{item}]'
                Bits.__cache__[item] = type(type_name, (cls,), {'Length': item})
                return Bits.__cache__[item]
        raise TypeError(f"Bits type only accept int type for Bits[N], not {type(item)}")

    @classmethod
    def castfrom(cls, value)->'Bits|None':
        if issubclass(type(value), Bits):
            return value
        elif isinstance(value, int):
            return Bits(tuple(bin(value)[2:]))
        elif isinstance(value, str):
            return cls(tuple(value))
        elif isinstance(value, list):
            return cls(tuple(['1' if i else '0' for i in value]))
        return None

    def __len__(self):
        return len(self.bits)

    def toint(self):
        return int(''.join(self.bits), 2)

    @classmethod
    def check(cls, value):
        print("*", value.__class__, issubclass(value.__class__, Bits))
        if issubclass(value.__class__, Bits):
            return value.Length == cls.Length
        return False

    def __getitem__(self, index):
        if isinstance(index, slice):
            s, e = index.start, index.stop
            s = s if s else 0
            e = e if e else len(self.bits)
            print("get", s, "to", e, self.bits[s:e])
            if s > e:
                return Bits(self.bits[s:e-1:-1])
            return Bits(self.bits[s:e])
        return self.bits[index]

    def __setitem__(self, index, value):
        bitsvalue = Bits.castfrom(value)
        if bitsvalue:
            value = bitsvalue.bits
            if isinstance(index, slice):
                s, e = index.start, index.stop
                s = s if s else 0
                e = e if e else len(self.bits)
                if s > e:
                    self.bits = (*self.bits[:e], *value[::-1], *self.bits[s+1:])
                else:
                    self.bits = (*self.bits[:s], *value, *self.bits[e+1:])
            else:
                self.bits = (*self.bits[:index], *value, *self.bits[index+1:])

    def __repr__(self):
        return f'{self.__class__.__name__}({self.bits})'

    def __eq__(self, other):
        for a, b in zip(self.bits, other.bits):
            if a != b:
                return False
        return True

# Bits[10](0, 1, 0, 1, 0, 1, 0, 1, 0, 1)


