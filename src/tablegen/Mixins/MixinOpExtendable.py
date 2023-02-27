
def ExtendOp(cls, func, Op):
    setattr(cls, Op, func)
    return func

class __MixinOpExtendable__:
    
    @classmethod
    def extendOp(cls, name, *args):
        cls.ExtendableOp(name, f"__{name}__")
        for alias in args:
                cls.ExtendableOp(alias, f"__{name}__")

    @classmethod
    def ExtendableOp(cls, name, Op):
        @classmethod
        def _func_(cls, func):
            ExtendOp(cls, func, Op)
        setattr(cls, name, _func_)

class MixinOpExtendable(__MixinOpExtendable__):
    pass

