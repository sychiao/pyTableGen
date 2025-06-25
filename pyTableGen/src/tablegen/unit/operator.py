class Operator:
    def __init__(self, opcode, *args):
        self.opcode = opcode
        self.args = args

    def __call__(self):
        raise NotImplementedError

class Not(Operator):
    def __init__(self, v):
        self.v = v 

    def __call__(self):
        raise NotImplementedError

class Add(Operator):
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return f'({self.a} + {self.b})'
    
    def __call__(self):
        return self.a() + self.b()

class Getter(Operator):

    def __init__(self, obj, name):
        self.obj = obj
        self.name = name

    def __str__(self):
        return self.name
    
    def __call__(self):
        return self.obj.__dict__[self.name]

class Value(Operator):

    def __init__(self, ctx, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __call__(self):
        return self.value

class AttributeSetter:

    def __init__(self, attr_setters: dict[str, Operator]):
        self.attr_setters = attr_setters

    def __call__(self, obj):
        for attr, setter in self.attr_setters.items():
            setattr(obj, attr, setter())