from types import SimpleNamespace
from typing import Any
from ..wrapper.recordkeeper import RecordKeeper
import tablegen.wrapper.recordkeeper as RK
import types
from .record import TDRecord, UnionTDRecord, TblRecMetaData
import tablegen.unit.dag as dag

class TBLParser:

    def __init__(self, Recs):
        self.Recs = Recs
        self.TDRecordMapping = dict()
        self.TDRecordTypeMapping = dict()

    def getTDRecord(self, rec):
        if rec not in self.TDRecordMapping:
            tdrec = self.convertTableGenRecordWrapper2TDRecord(rec)
            self.TDRecordMapping[rec] = tdrec
        return self.TDRecordMapping[rec]

    def getTDRecordType(self, reccls):
        if reccls not in self.TDRecordTypeMapping:
            tdrec = self.convertTableGenClassWrapper2TDRecordType(reccls)
            self.TDRecordTypeMapping[reccls] = tdrec
        return self.TDRecordTypeMapping[reccls]
    
    def convertTableGenRecordWrapper2TDRecord(self, rec, TDRecMap=dict()):
        # print("Converting TableGenRecordWrapper to TDRecord", rec)
        clslst = [self.TDRecordTypeMapping[cls] for cls in rec.getBaseClasses()]
        tdreccls = UnionTDRecord(*clslst) if len(clslst) > 1 else clslst[0]
        obj = tdreccls.create()
        for key, valu in rec.items.items():
            if isinstance(valu, RK.TableGenRecord):
                setattr(obj, key, self.getTDRecord(valu))
            else:
                setattr(obj, key, valu)
        return obj

    def convertTableGenClassWrapper2TDRecordType(self, reccls, TDRecMap=dict()):
        # print("Converting TableGenClassWrapper to TDRecordType", reccls)
        # print("bases: ")
        bases = []
        for base in reccls.bases:
            bases.append(self.getTDRecordType(self.Recs.getClass(base)))
        metadata = TblRecMetaData()
        metadata.name = reccls.defname
        metadata.signature = tuple(reccls.args().items())
        metadata.fields = {name: self.castValue(ty) for name, ty in reccls.fields.items() if ':' not in name}
        print("metadata.fields:", metadata.fields)
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
        else:
            return _value

class RecordContext(SimpleNamespace):

    def load(self, RK: RecordKeeper):
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        value.tbl.name = name
        return super().__setattr__(name, value)