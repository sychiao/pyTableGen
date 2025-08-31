from types import ModuleType
from typing import Any
from ..wrapper.recordkeeper import RecordKeeper
import tablegen.wrapper.recordkeeper as RK
import types
from .record import TDRecord, UnionTDRecord, TblRecMetaData, _Record
import tablegen.unit.dag as dag
from collections import defaultdict, deque
import sys

from .dumper import dumpDef

class TBLParser:

    def __init__(self, Recs: RecordKeeper):
        self.file = Recs._RK.getInputFilename()
        self.Recs = Recs
        self.TDRecordMapping = dict()
        self.TDRecordTypeMapping = dict()

    def getTDRecord(self, rec):
        if rec not in self.TDRecordMapping:
            return self.convertTableGenRecordWrapper2TDRecord(rec)
        return self.TDRecordMapping[rec]

    def getTDRecordType(self, reccls):
        # print("getTDRecordType: ", reccls)
        # print("Bases:", reccls.bases)
        if reccls not in self.TDRecordTypeMapping:
            tdrec = self.convertTableGenClassWrapper2TDRecordType(reccls)
            self.TDRecordTypeMapping[reccls] = tdrec
            for name, ty in tdrec.tbl.fields.items():
                tdrec.tbl.fields[name] = self.castValue(ty)
            tdrec.tbl.signature = tuple((n, self.castValue(t)) for n, t in tdrec.tbl.signature)
        return self.TDRecordTypeMapping[reccls]
    
    def convertTableGenRecordWrapper2TDRecord(self, rec, TDRecMap=dict()):
        # print("Converting TableGenRecordWrapper to TDRecord", rec)
        clslst = [self.TDRecordTypeMapping[cls] for cls in rec.getBaseClasses()]
        if clslst:
            tdreccls = UnionTDRecord(*clslst) if len(clslst) > 1 else clslst[0]
        else:
            tdreccls = TDRecord
        obj = tdreccls.create()
        # print("obj:", obj, "get items:", id(rec))
        # print(rec.items)
        obj.tbl.file = self.file
        self.TDRecordMapping[rec] = obj
        for key, valu in rec.items.items():
            if isinstance(valu, RK.TableGenRecord):
                setattr(obj, key, self.getTDRecord(valu))
            else:
                setattr(obj, key, valu)
        return obj

    def convertTableGenClassWrapper2TDRecordType(self, reccls, TDRecMap=dict()):
        bases = []
        for base in reccls.bases:
            # print(">> Bases:", base)
            bases.append(self.getTDRecordType(self.Recs.getClass(base)))
        metadata = TblRecMetaData()
        metadata.name = reccls.defname
        metadata.file = self.file
        metadata.signature = tuple(reccls.args().items())
        metadata.fields = {name: ty for name, ty in reccls.fields.items() if ':' not in name}
        if bases:
            return types.new_class(reccls.defname, tuple(bases), {'metadata': metadata})
        else:
            return types.new_class(reccls.defname, (TDRecord, ), {'metadata': metadata})
    
    def castValue(self, _value):
        if isinstance(_value, RK.TableGenClassWrapper):
            return self.getTDRecordType(_value)
        elif isinstance(_value, RK.TableGenRecordWrapper):
            return self.getTDRecord(_value)
        elif isinstance(_value, dag.DAG):
            new_dag = dag.DAG(self.castValue(_value.op))
            for name, node in _value.nodes.items():
                new_dag.nodes[name] = dag.Node(node.name, self.castValue(node.value))
            return new_dag
        elif isinstance(_value, list):
            return [self.castValue(v) for v in _value]
        elif isinstance(_value, types.GenericAlias):
            return _value.__origin__[*(self.castValue(arg) for arg in _value.__args__)]
        else:
            return _value
        
    def parse(self):
        for name, cls in self.Recs.getClasses().items():
            ty = self.getTDRecordType(cls)
            yield name, ty
        for rec in self.Recs.getDefs():
            tdrec = self.getTDRecord(rec)
            yield rec.defname, tdrec

class RecordContext(ModuleType):

    def __init__(self, name = "RecordContext"):
        super().__init__(name)
        self.RK = None
        self.lazy = False
        self.__classesMapping = dict()
    
    def gen_typing_stubs(self, file=sys.stdout):
        if self.RK:
            indegree = defaultdict(int)
            graph = defaultdict(set)
            rec_lst = list()
            for name, value in TBLParser(self.RK).parse():
                if isinstance(value, type) and issubclass(value, TDRecord):
                    if name in self.__dict__:
                        name = f"{name}Class"
                    if name not in graph:
                        graph[name] = set()
                    setattr(self, name, value)
                    for base in value.__bases__:
                        if base is TDRecord:
                            continue
                        if issubclass(base, TDRecord):
                            graph[base.__name__].add(value.__name__)
                            indegree[value.__name__] += 1
                        
                else:
                    if name in self.__dict__ and isinstance(getattr(self, name), type):
                        name = f"{name}Record"
                    setattr(self, name, value)
                    rec_lst.append(f"{name}: '{type(value).__name__}'")
        
            print('### Typing stubs generated by pyTableGen ###', file=file)
            print("from tablegen.dsl.record import TDRecord, UnionTDRecord", file=file)
            print("from tablegen.unit.dag import DAG", file=file)
            print("from tablegen.unit.bits import Bits", file=file)

            print('Predicate in class lst?', 'Predicate' in self.__dict__)
            print(indegree['Predicate'], getattr(self, 'Predicate', None))

            q = deque([cls for cls in graph if indegree[cls] == 0])
            print("Initial zero indegree classes:", list(q))
            class_lst = []
            while q:
                cls = q.popleft()
                class_lst.append(cls)
                for nei in graph[cls]:
                    indegree[nei] -= 1
                    if indegree[nei] == 0:
                        q.append(nei)

            print(">>", 'Predicate' in class_lst)
            
            for clsname in class_lst:
                cls = getattr(self, clsname)
                def dump_type_name(v):
                    if isinstance(v, types.GenericAlias):
                        return f"{v.__origin__.__name__}[{', '.join(dump_type_name(arg) for arg in v.__args__)}]"
                    elif isinstance(v, type):
                        return v.__name__
                    else:
                        return type(v).__name__
                fields = "\n".join(f"    {k}: '{dump_type_name(v)}'" for k, v in cls.tbl.fields.items())
                signature = ", ".join(f"{k}: '{dump_type_name(v)}'" for k, v in cls.tbl.signature)
                print(f"class {cls.__name__}({', '.join(base.__name__ for base in cls.__bases__)}):\n"
                                 f"{fields if fields else ''}\n"
                                 f"    def __init__(self, {signature}): ...\n\n", file=file)
            for rec in rec_lst:
                print(rec, file=file)

    @classmethod
    def load(cls, RK: RecordKeeper, lazy=False):
        ctx = cls()
        if not lazy:
            for name, value in TBLParser(RK).parse():
                setattr(ctx, name, value)
        ctx.RK = RK
        ctx.lazy = lazy
        return ctx
    
    def __getattr__(self, name: str) -> Any:
        if self.lazy and self.RK is not None:
            rec = self.RK.getRecord(name) 
            reccls = self.RK.getClass(name)
            if reccls and rec:
                tdrec = TBLParser(self.RK).castValue(rec)
                setattr(self, name+'Record', tdrec)
                tdreccls = TBLParser(self.RK).castValue(reccls)
                setattr(self, name+'Class', tdreccls)
                return (reccls, rec)
            elif rec:
                tdrec = TBLParser(self.RK).castValue(rec)
                setattr(self, name, tdrec)
                return tdrec
            elif reccls:
                tdreccls = TBLParser(self.RK).castValue(reccls)
                setattr(self, name, tdreccls)
                return tdreccls
        raise AttributeError(f"RecordContext has no attribute {name}")
    
    def getRecordsByType(self, reccls):
        if reccls.__name__ in self.__classesMapping:
            return self.__classesMapping.get(reccls.__name__, [])
        lst = [obj for obj in self.__dict__.values() \
                if isinstance(obj, _Record) and isinstance(obj, reccls)]
        self.__classesMapping[reccls.__name__] = lst
        return lst

    def __setattr__(self, name: str, value: Any) -> None:
        if isinstance(value, _Record):
            value.tbl.name = name
        return super().__setattr__(name, value)
    
    def dump(self, file, objs):
        if objs is None:
            self.dumpAll(file)
        else:
            if isinstance(file, str):
                with open(file, 'a') as f:
                    self.dump(f, objs)
            else:
                for obj in objs:
                    if obj not in self.__dict__.values():
                        raise ValueError(f"Object {obj} is not in the context")
                  
                for obj in merge_ordered_lists(self.dumpOrder(obj) for obj in objs):
                    if obj.tbl.file is not None:
                        raise ValueError(f"Object {obj} has been dumped to {obj.tbl.file}, cannot dump again")
                    obj.tbl.file = file.name
                    print(dumpDef(obj), file=file)

    def dumpOrder(self, obj, lst=None):
        lst = lst or deque()
        lst.append(obj)
        for k, v in obj.__dict__.items():
            if isinstance(v, _Record):
                self.dumpOrder(v, lst)
        return list(reversed(lst))

def merge_ordered_lists(lists):
    # 建圖
    graph = defaultdict(set)
    indegree = defaultdict(int)

    for lst in lists:
        for a, b in zip(lst, lst[1:]):
            if b not in graph[a]:  # 避免重複邊
                graph[a].add(b)
                indegree[b] += 1
            indegree.setdefault(a, 0)  # 確保 a 也在 indegree 裡

    # 拓撲排序 (Kahn’s algorithm)
    q = deque([n for n, d in indegree.items() if d == 0])
    result = []
    while q:
        node = q.popleft()
        result.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)

    return result
