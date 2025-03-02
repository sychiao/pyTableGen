from typing import overload
from ._base import TableGenType, Unset
class VarBit(TableGenType):
    Owner: 'Bits'

    def __init__(self, Owner, index):
        self.Owner = Owner
        self.index = index
    
    def value(self) -> 'str|None':
        if isinstance(v := self.Owner[self.index], str):
            return v
        return None
    
    def __eq__(self, other):
        if isinstance(other, VarBit):
            return self.Owner.defname == other.Owner.defname and self.index == other.index
        return self.value() == other

    def __hash__(self) -> int:
        return hash((id(self.Owner), self.index))

    def __dump__(self):
        return f'{self.Owner.defname}[{self.index}]'

    def __repr__(self):
        if self.value():
            return f'{self.value()}'
        else:
            return f'{self.Owner.defname}[{self.index}]'        

class Bits(TableGenType):
    Length = -1
    bits: tuple
    __cache__ = dict()

    @staticmethod
    def toBit(bit):
        if isinstance(bit, VarBit):
            return bit
        elif not bit or bit == '0':
            return '0'
        else:
            return '1'

    def __init__(self, bits = None):
        if bits:
            def toBitInit(bit, idx):
                if isinstance(bit, Unset):
                    return VarBit(self, idx)
                return self.toBit(bit) 
            self.bits = \
                tuple([toBitInit(bit, idx) for idx, bit in enumerate(bits)])
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
        raise TypeError(f"Bits type only accept int, str, list or Bits type, not {type(value)}")

    def __len__(self):
        return len(self.bits)

    def toint(self):
        return int(''.join(self.bits), 2)

    @classmethod
    def check(cls, value):
        if issubclass(value.__class__, Bits):
            return value.Length == cls.Length
        return False

    @overload
    def __getitem__(self, index: int)->'str|VarBit':...

    @overload
    def __getitem__(self, index: slice)->'Bits':...

    def __getitem__(self, index):
        if isinstance(index, slice):
            s, e = index.start, index.stop
            s = s if s else 0
            e = e if e else len(self.bits)
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
        return all(a == b for a, b in zip(self.bits, other.bits))

    def __hash__(self) -> int:
        return hash(self.bits)

    def variables(self)->'set[Bits]':
        return {bit.Owner for bit in self.bits if isinstance(bit, VarBit)}

    def fragments(self)->'dict[tuple[int,int], Bits]':
        '''
        Fragments will try to divide bits to continuous bits or varbits with same variable.
        e.g.:
            {0, 1, 0, rs[0], rs[1]}
        it will divide to:
            (0:3): Bits({0, 1, 0}), (3:5): Bits({rs[0], rs[1]})
        '''
        fragments = dict()
        def saveFrag(frag, varStart, Start, End):
            if varStart >= 0:
                fragments[(Start, End)] = frag[varStart:varStart+(End-Start)]
            else:
                fragments[(Start, End)] = frag

        if isinstance(self.bits[0], VarBit):
            varStart, CurrFrag, FragStart = self.bits[0].index, self.bits[0].Owner, 0
        else:
            varStart, CurrFrag, FragStart = -1, Bits([self.bits[0]]), 0

        for idx, bit in enumerate(self.bits[1:], start=1):
            
            if isinstance(bit, VarBit):
                if bit.Owner != CurrFrag or bit.index - varStart != idx - FragStart:
                    saveFrag(CurrFrag, varStart, FragStart, idx)
                    varStart, CurrFrag, FragStart = bit.index, bit.Owner, idx
            else:
                if varStart >= 0:
                    saveFrag(CurrFrag, varStart, FragStart, idx)
                    varStart, CurrFrag, FragStart = -1, Bits([bit]), idx
                else:
                    CurrFrag.bits += (bit,)
        
        if CurrFrag:
            saveFrag(CurrFrag, varStart, FragStart, len(self.bits))
        
        return fragments

    @classmethod
    def __class_dump__(cls):
        return f'bits<{cls.Length}>' if cls.Length > 0 else f'bits<{len(cls.bits)}>'

    def __dump__(self):
        def bit2str(bit):
            if isinstance(bit, VarBit):
                return bit.__dump__()
            return bit
        return ''.join(bit2str(bit) for bit in self.bits)

    def getType(self):
        if (t:= type(self)) != Bits:
            return t
        return Bits[len(self.bits)]

    def isDef(self):
        for bit in self.bits:
            if isinstance(bit, VarBit):
                if bit.Owner is self:
                    return False
        return True

    def __iscomplex__(self):
        return len(self.fragments()) > 1

    def isVar(self):
        # Check if all bits are VarBits and they are from the same variable
        if not self.bits:
            return False

        first_owner = None
        for bit in self.bits:
            if not isinstance(bit, VarBit):
                return False
            if first_owner is None:
                first_owner = bit.Owner
            elif bit.Owner != first_owner:
                return False
        return True
    
    def isConstant(self):
        return all(isinstance(bit, str) for bit in self.bits)

    def concat(self, other):
        return Bits(self.bits + other.bits)

    def __matmul__(self, other):
        # @ is used for concatenation bits
        return self.concat(other)

    def __add__(self, other):
        # + is used for add bits
        return Bits(hex(self.toint() + other.toint())[2:])

# Bits[10](0, 1, 0, 1, 0, 1, 0, 1, 0, 1)


