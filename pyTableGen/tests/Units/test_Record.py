from tablegen.unit.record import TypedRecord, TableGenRecord
from tablegen.unit.bits import Bits
from dataclasses import dataclass, field
from tablegen.dumper import dumpTblRecord

@dataclass
class A(TypedRecord):
    x: int
    y: int

    def __post_init__(self):
        self.v = self.x + self.y

def test_1():
    print(issubclass(A, TypedRecord))
    A.a = A(1, 2).let("a", 3)
    A.a.let("b", Bits[5]()).let("c", Bits[5]('01011')).let("d", A.a.b)
    A.a.additional_fields()
    print(A.a)
    print(dumpTblRecord(A.a))
