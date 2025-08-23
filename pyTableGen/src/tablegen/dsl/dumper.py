from .record import PyRecord, TDRecord, UnionRecord

def dumpRecordConstructVal(rec) -> str:
    if isinstance(rec, UnionRecord):
        return ', '.join(dumpRecordConstructVal(rec) for rec in rec.recs)
    elif isinstance(rec, TDRecord):
        raise TypeError("TDRecord cannot be dumped directly")
    else:
        if rec.tbl.args:
            return f"{rec.__class__.__name__}<{', '.join(repr(arg) for arg in rec.tbl.args)}>"
        else:
            return f"{rec.__class__.__name__}"

def dumpDef(rec, name=None):
    name = name or rec.tbl.name
    if rec.tbl.extra:
        body = list()
        body.extend([f"\t{type(v).__name__} {k};" for k, v in rec.tbl.extra.items() if k not in rec.fields])
        body.extend([f"\tlet {k} = {v!r};" for k, v in rec.tbl.extra.items()])
        bodyStr = " {\n" + "\n".join(body) + "\n}"
    else:
        bodyStr = ";"
    return f"def {name} : {dumpRecordConstructVal(rec)}{bodyStr}"