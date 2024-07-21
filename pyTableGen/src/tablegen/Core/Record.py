from Dyne.dyn import DynClass, DynFunc, DynModule

class RecordClass:
    init_args: dict
    __init_func: DynFunc

    @staticmethod
    def init_func(name, *args):
        return f'''{name}.__init__(self, {", ".join(args)})'''

    def __init__(self, name):
        self.__name__ = name
        self.init_args = dict()
        self.__bases__ = ["Record"]
        self.__dynmethods = dict()
        self.__dynbody = dict()
        self.__dyncls = DynClass(name, self.__bases__, self.__dynbody, self.__dynmethods)

    def init(self, **kwargs):
        self.init_args = kwargs
        self.__dynmethods['__init__'] = DynFunc("__init__", self.init_args, [])
        return self

    def add_init(self, cls_name, *args):
        self.__bases__.append(cls_name)
        self.__dynmethods['__init__'].body.append(RecordClass.init_func(cls_name, *args))
        return self

    def dump(self):
        return self.__dyncls._getSrc()

    def get_dyncls(self):
        return self.__dyncls

class Record:

    def __init__(self, name):
        self.__name__ = name
    
    def __name__(self):
        pass

    def isClass(self):
        pass


import types
m = types.ModuleType('name')
print(m, m.__dict__)

'''
class ProcNoItin<string Name, list<SubtargetFeature> Features> : Processor<Name, NoItineraries, Features>;
=>
RecordClass("ProcNoItin")
    .init(Name, str, Features, list<SubtargetFeature>)
    .add_init(Processor, Name, NoItineraries, Features)

 init = 
    def __init__(Name: str, Features: list<SubtargetFeature>)
        Processor.__init__(Name, NoItineraries, Features)
 inherit = 
    Processor
)
'''

s = RecordClass("ProcNoItin")\
    .init(Name="'str'", Features="'list[SubtargetFeature]'")\
    .add_init("Processor", "Name", "NoItineraries", "Features")

a = RecordClass("Processor")\
    .init(Name="'str'", Itin="'str'", Features="'list[SubtargetFeature]'")

print(s.dump())
print(a.dump())

m = DynModule("A", {"ProcNoItin": s.get_dyncls(), "Processor": a.get_dyncls()})
m.add("Record", Record)
m._getIns()

#a = Record("name")
#print(a.__name__)


# Create RecordClass with name Instruction
# add init function with arguments Name, Opcode, Operands, Properties
#RecordClass("Instruction")\
#    .init(Name="str", Opcode="int", Operands="list<Operand>", Properties="list<Property>")
    
