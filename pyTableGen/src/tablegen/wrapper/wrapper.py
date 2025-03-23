from tablegen.unit.record import TableGenRecord
import weakref

class Wrapper:
    __cached__ = weakref.WeakValueDictionary()

    def __init_subclass__(cls):
        cls.__cached__ = weakref.WeakValueDictionary()

    def __new__(cls, obj, *args):
        if cached := cls.__cached__.get(id(obj)):
            return cached
        if issubclass(obj.__class__, TableGenRecord):
            return obj
        ins = super().__new__(cls)
        cls.__cached__[id(obj)] = ins
        return ins

    @classmethod
    def wrap(cls, obj):
        if cached := cls.__cached__.get(id(obj)):
            return cached
        cls.__cached__[id(obj)] = ins = cls(obj)
        return ins