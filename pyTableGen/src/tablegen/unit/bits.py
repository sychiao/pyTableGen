from ._base import TableGenType

class Bits(TableGenType):
    Length = -1
    __cache__ = dict()

    def __init__(self, bits = None):
        self.bits = bits
        if bits and self.Length > 0:
            if len(bits) != self.Length:
                raise ValueError(f"Bits[{self.Length}] must have {self.Length} bits, not {len(bits)}")

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
            return Bits(bin(value)[2:])
        elif isinstance(value, str):
            return cls(value)
        elif isinstance(value, list):
            return cls(''.join(['1' if i else '0' for i in value]))
        return None

    @classmethod
    def check(cls, value):
        if v := Bits.castfrom(value):
            if cls.Length > 0:
                return len(v) == cls.Length
            return True
        return False

    def __len__(self):
        return len(self.bits)

    def toint(self):
        return int(f'{self.bits}', 2)

    def __getitem__(self, index):
        if isinstance(index, slice):
            s, e = index.start, index.stop
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
                if s > e:
                    self.bits = f"{self.bits[:e]}{value[::-1]}{self.bits[s+1:]}"
                else:
                    self.bits = f"{self.bits[:s]}{value}{self.bits[e+1:]}"
            # print(index, value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.bits})'


# Bits[10](0, 1, 0, 1, 0, 1, 0, 1, 0, 1)


