from typing import Any, overload
from .value import Unset

class VarBit:
    Owner: 'Bits'

    def __init__(self, Owner: 'Bits', index):
        self.Owner = Owner
        self.index = index
    
    def value(self) -> 'str|None':
        if isinstance(v := self.Owner[self.index], str):
            return v
        return None
    
    def __eq__(self, other):
        if isinstance(other, VarBit):
            return self.Owner.name == other.Owner.name and self.index == other.index
        return self.value() == other

    def __hash__(self) -> int:
        return hash((id(self.Owner), self.index))

    def __dump__(self):
        return f'{self.Owner.name}{{{self.index}}}'

    def __repr__(self):
        if self.value():
            return f'{self.value()}'
        else:
            return f'{self.Owner.name}[{self.index}]'        

class BitsMeta(type):

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        obj = super().__call__(*args, **kwds)
        assert issubclass(type(obj), Bits)
        assert type(obj) is not Bits
        return obj

    def __instancecheck__(self, value: Any) -> bool:
        return issubclass(value.__class__, Bits)\
            and (self.Length == 0 or value.Length == self.Length)

class Bits:
    '''
    Bits type, can be defined as Bits[N] or Bits('0101') or Bits(0b1010) or Bits([0,1,0,1])
    Bits type, can be variable bit, e.g. Bits[5]('rd')
    Bits([0, 1, 0, rd[0], rd[1], 0, 1])
    Bits can be concatenated with @ operator, e.g. Bits('0101') @ Bits('1010')
    Bits can be added with + operator, e.g. Bits('0101') + Bits('1010') = Bits('00011111')
    '''
    name: str
    Length = -1
    bits: tuple
    __BitsTypesCache = dict()

    @staticmethod
    def toBit(bit):
        if isinstance(bit, VarBit):
            return bit
        elif not bit or bit == '0':
            return '0'
        else:
            return '1'

    def __init__(self, bits_or_name = None):
        if isinstance(bits_or_name, str):
            if bits_or_name[0].isdigit():
                assert all(map(lambda x: x.isdigit(), bits_or_name))
                bits, name = tuple(bits_or_name), None
            else:
                bits, name = None, bits_or_name
        else:
            bits, name = bits_or_name, None

        self.name = name

        if bits:
            def toBitInit(bit, idx):
                if isinstance(bit, Unset):
                    return VarBit(self, idx)
                return self.toBit(bit) 
            self.bits = \
                tuple([toBitInit(bit, idx) for idx, bit in enumerate(bits)])
        else:
            self.bits = tuple([VarBit(self, i) for i in range(self.Length)])

        if self.Length > 0:
            if len(self.bits) != self.Length:
                raise ValueError(f"Bits[{self.Length}] must have {self.Length} bits, not {len(bits)}")
        else:
            self.__class__ = Bits[len(self.bits)] # implict cast to Bits[N]

    def __class_getitem__(cls, item):
        if isinstance(item, int):
            if cs := Bits.__BitsTypesCache.get(item):
                return cs
            else:
                type_name = f'{cls.__name__}[{item}]'
                Bits.__BitsTypesCache[item] = type(type_name, (cls,), {'Length': item})
                return Bits.__BitsTypesCache[item]
        raise TypeError(f"Bits type only accept int type for Bits[N], not {type(item)}")

    def __len__(self):
        return len(self.bits)

    def toint(self):
        return int(''.join(self.bits), 2)

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
            return Bits(self.bits[s:e+1])
        return self.bits[index]

    def __setitem__(self, index, value):
        bitsvalue = Bits.castfrom(value)
        if bitsvalue:
            value = bitsvalue.bits
            if isinstance(index, slice):
                s, e = index.start, index.stop
                s = s if s else 0
                e = e if e else len(self.bits)
                if (abs(s - e) + 1) != len(value):
                    raise ValueError(f"Cannot assign {len(value)} bits to slice of length {(abs(s - e) + 1)}")
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

    def isVar(self):    
        return  all(isinstance(bit, VarBit) for bit in self.bits) \
            and len(self.variables()) == 1

    def isConstant(self):
        return all(isinstance(bit, str) for bit in self.bits)

    def concat(self, other):
        return Bits(self.bits + other.bits)

    def __matmul__(self, other):
        # @ is used for concatenation bits
        return self.concat(other)
    
    @classmethod
    def castfrom(cls, value)->'Bits':
        if issubclass(type(value), Bits):
            return value
        elif isinstance(value, int):
            return Bits(tuple(bin(value)[2:]))
        elif isinstance(value, str):
            return cls(tuple(value))
        elif isinstance(value, list):
            return cls(tuple(['1' if i else '0' for i in value]))
        raise TypeError(f"Bits type only accept int, str, list or Bits type, not {type(value)}")

    def fragments(self: 'Bits')->'dict[tuple[int,int], Bits]':
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