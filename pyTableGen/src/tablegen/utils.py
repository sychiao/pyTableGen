def LazyAttr(f):
    def Attrf(self):
        try:
            return getattr(self, f'__{f.__name__}')
        except AttributeError:
            setattr(self, f'__{f.__name__}', f(self))
            return getattr(self, f'__{f.__name__}')
    return Attrf

def LazyProperty(f):
    return property(LazyAttr(f))

class CacheDict:
    '''
    A CacheDict is a dictionary that provide __getf__ to get value like dict, and save result with real dict as cache.
    '''

    def __init__(self):
        self.__cache__ = dict()

    def __getf__(self, key):
        raise NotImplementedError

    def __getitem__(self, key):
        if key not in self.__cache__:
            if ins := self.__getf__(key):
                self.__cache__[key] = ins
                return ins
            raise KeyError(f"{key} not in CacheDict")
        else:
            return self.__cache__[key]

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            return default