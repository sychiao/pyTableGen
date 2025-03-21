from collections.abc import Sequence
from tablegen.unit.record import TableGenRecord

class Node:
    __match_args__ = ('name', 'value')
    value: TableGenRecord

    def __init__(self, name=None, value=None):
        assert value is not None or name is not None
        self.value = value
        self.name = name

    def __repr__(self):
        return f'{self.value}:${self.name}'

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        return self.value == other

class DAG(Sequence):
    __match_args__ = ('op', 'nodes')
    op: TableGenRecord
    nodes: dict[str, Node]

    def __init__(self, op, *args, **nodes):
        self.op = op
        self.nodes = nodes
        for idx, arg in enumerate(args):
            nodes[f'{idx}'] = arg

    def __getitem__(self, key): # type: ignore (syntax suger)
        if key == '_op':
            return self.op
        return Node(str(key), self.nodes[str(key)])
    
    def __iter__(self):
        yield self.op
        for item in self.nodes.items():
            yield Node(*item)

    def __contains__(self, key: object) -> bool:
        return key == '_op' or key in self.nodes
    
    def keys(self):
        yield '_op'
        yield from self.nodes.keys()

    def items(self):
        for item in self.nodes.items():
            yield Node(*item)
    
    def __len__(self) -> int:
        return len(self.nodes) + 1

    def __repr__(self):
        return f'DAG({self.op.defname} {", ".join(map(str, self.items()))})'
        


