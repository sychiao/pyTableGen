import pytest
from tablegen.Mixins.MixinOpExtendable import MixinOpExtendable

def test_basicUsage():
    class A(MixinOpExtendable):
        pass

    a1 = A()
    a2 = A()

    with pytest.raises(Exception) as e_info:
        a1["hello"] # assert
        a1 | a2 # assert

    
    with pytest.raises(Exception) as e_info:
        @A.getitem
        def _(cls, name):
            return name

    MixinOpExtendable.extendOp("add")
    MixinOpExtendable.extendOp("or", "union")
    MixinOpExtendable.extendOp("getitem")
    MixinOpExtendable.extendOp("sub")

    @A.getitem
    def _(cls, name):
        return name

    @A.union
    def _(cls, other):
        return other
    
    @A.add
    def _(cls, other):
        return print("add")
    
    @A.sub
    def _(cls, other):
        return print("sub")

    a1["hello"] # assert
    a1 | a2 # assert
    a1 + a2
    a1 - a2