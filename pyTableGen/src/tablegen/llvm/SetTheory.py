from ..unit.record import TableGenRecord
from tablegen.unit.dag import DAG, Node

class SetTheory:
    '''
    Set Theory for TableGen, binding setthoery with tablegen is not easy
    it's a reimplementation of the TableGen set theory in python
    Notice, this is a simple implementation, it's not complete
    it's only resolve records name, but you can retrieve the records from the RecordKeeper
    some expander like registertuples it will add implicit records,
    you need handle it when you use these records
    '''

    def __init_subclass__(cls) -> None:
        cls.expander = dict()
        for e, f in cls.__dict__.items():
            if e.startswith("expand") and callable(f):
                cls.expander[e.replace('expand','')] = f

    def __init__(self, recs):
        self.recs = recs

    def expand(self, member: DAG | Node | TableGenRecord) -> set[str]:
        if isinstance(member, TableGenRecord):
            for clsname in member.classes:
                if clsname in self.expander:
                    return self.expander[clsname](self, member)
            raise NotImplementedError(f"Expand {member.defname} {member.classes} is not NotImplemented")
        elif isinstance(member, Node):
            return self.expand(member.value)
        else:
            match member:
                case (self.recs.add, *ops):
                    return set([r for op in ops for r in self.expand(op)])
                case (self.recs.sequence, strfmt, start, end):
                    return set([strfmt.value.replace("%u", str(idx)) for idx in range(start.value, end.value)])
                case (self.recs.sequence, strfmt, start, end, step):
                    return set([strfmt.value.replace("%u", str(idx)) for idx in range(start.value, end.value, step.value)])
                case (self.recs.sub, base, *ops):
                    return self.expand(base) - set([r for op in ops for r in self.expand(op)])
                case (op, *args):
                    raise NotImplementedError(f"({op.defname} with {len(args)} nodes) is not NotImplemented")
                case _:
                    raise ValueError(f"set thoery must be (op, *args) pattern", member)
