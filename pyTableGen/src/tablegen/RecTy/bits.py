from .type import TableGenType

class Bits(TableGenType):
    Length = -1

    def __init__(self, bits):
        self.bits = bits

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
        if isinstance(index, slice):
            s, e = index.start, index.stop
            if s > e:
               self.bits = f"{self.bits[:e]}{value[::-1]}{self.bits[s+1:]}"
            self.bits = f"{self.bits[:s]}{value}{self.bits[e+1:]}"
        print(index, value)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.bits})'

a = Bits('01011')
print(isinstance(a, Bits))
#print(isinstance(1, Bits))
print(isinstance(a, Bits[5]))


if a := Bits.castfrom(1902):
  print(a.toint())
  print(a.bits)
  print(a[1:4])
  print(a[4:1])
  #a[1:4] = '1234'
  a[4:1] = '1234'
  print(a)
  print(a[1:4])
# Bits[10](0, 1, 0, 1, 0, 1, 0, 1, 0, 1)


