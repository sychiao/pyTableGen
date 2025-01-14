class MetaTableGenType(type):
    __types__: dict[str, type] = dict()

    def __instancecheck__(cls, instance, /) -> bool:
        print('instance check', cls.__name__, cls.check(instance))
        return cls.check(instance)

    def check(cls, instance):
        return super().__instancecheck__(instance)

class TableGenType(metaclass=MetaTableGenType):
    pass

class RecordType(TableGenType):

    def check(cls, instance):
        pass

