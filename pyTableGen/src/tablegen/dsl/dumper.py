from .record import PyRecord, TDRecord, UnionRecord, _Record
from ..unit.dag import DAG


def dumpRecordConstructVal(rec) -> str:
    if isinstance(rec, UnionRecord):
        return ', '.join(dumpRecordConstructVal(rec) for rec in rec.recs)
    else:
        if rec.tbl.args:
            return f"{rec.__class__.__name__}<{', '.join(repr(arg) for arg in rec.tbl.args)}>"
        else:
            return f"{rec.__class__.__name__}<>"
        
def dumpValue(val) -> str:
    if isinstance(val, int):
        return str(val)
    elif isinstance(val, str):
        return repr(val)
    elif isinstance(val, _Record):
        if val.tbl.name:
            return val.tbl.name
        else:
            return dumpRecordConstructVal(val)

def dumpDef(rec, name=None):
    name = name or rec.tbl.name or ""
    if rec.tbl.extra:
        body = list()
        body.extend([f"\t{type(v).__name__} {k};" for k, v in rec.tbl.extra.items() if k not in rec.fields])
        body.extend([f"\tlet {k} = {dumpValue(v)};" for k, v in rec.tbl.extra.items()])
        bodyStr = " {\n" + "\n".join(body) + "\n}"
    else:
        bodyStr = ";"
    return f"def {name} : {dumpRecordConstructVal(rec)}{bodyStr}"