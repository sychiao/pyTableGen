from tablegen.dsl.record import PyRecord, TDRecord, TblRecMetaData, UnknownValue, UnionTDRecord
from tablegen.dsl.context import RecordContext
from tablegen.dsl.dumper import dumpDef

def test_1():
    class Rec(PyRecord):
        val: str

        def __init__(self, val: str):
            self.val = val

    class RecX(PyRecord):
        val: str

        def __init__(self, val: str):
            self.val = val

    class RecY(RecX):
        index: int

        def __init__(self, val: str):
            super().__init__(val)
            self.index = len(val)

    ctx = RecordContext()
    new_cls = type('NewRecord', (PyRecord,), {'__name__': 'NewRecord'})
    ctx.x = Rec('A') | RecY('B')
    ctx.x.val = 123
    ctx.x.extra = 123

    assert isinstance(ctx.x, Rec)
    assert isinstance(ctx.x, RecX)
    assert not isinstance(ctx.x, new_cls)

    golden = '''
def x : Rec<'A'>, RecY<'B'> {
\tint extra;
\tlet val = 123;
\tlet extra = 123;
}'''
    assert golden.replace('\n','').replace('\t','') == \
            dumpDef(ctx.x).replace('\n','').replace('\t','')

    # ctx.x only contains extra, value, index and _recs, and _tbl
    assert len(ctx.x.__dict__) == 5
    assert ctx.x.val == 123

def test_2():
    print("=========== Test TDRecord ===========")
    # Test TDRecord with metadata
    import types
    metadata = TblRecMetaData()
    metadata.fields = {'name': str, 'value': int}
    metadata.signature = (('name', int), ('value', None))
    NewTDRecord = types.new_class("NewTDRecord", (TDRecord, ), {'metadata': metadata})

    class pyNewRecord(NewTDRecord):
        
        def __init__(self, name: str, value: int = 0):
            self.name = name
            self.value = value

    val = NewTDRecord('Test', 123)
    print(val.name)
    assert isinstance(val.name, UnknownValue)
    val = pyNewRecord('Test', 123)
    assert val.name == 'Test'
    assert isinstance(val, NewTDRecord)