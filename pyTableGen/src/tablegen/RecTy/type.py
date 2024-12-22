class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __getitem__(cls, arg):
        clsname = f'{cls.__name__}[{arg}]'
        try:
            return cls.__types__[clsname]
        except KeyError:
            cls.__types__[clsname] = type(f'{cls.__name__}[{arg}]', (cls,), {'Args': arg})
            return cls.__types__[clsname]

    def __instancecheck__(cls, instance, /) -> bool:
        print('instance check', cls.__name__, cls.check(instance))
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)

class TableGenType(metaclass=MetaTableGenType):
    pass