def LazyAttr(f):
    def Attrf(self):
        try:
            return getattr(self, f'__{f.__name__}')
        except:
            setattr(self, f'__{f.__name__}', f(self))
            return getattr(self, f'__{f.__name__}')
    return Attrf

def LazyProperty(f):
    return property(LazyAttr(f))