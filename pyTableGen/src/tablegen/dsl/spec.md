# pyTableGen DSL

pyTablGen DSL is a interface to 'read/write tablegen'.

* What's different of wrapper?
    - `wrapper` is override '__getattr__' to access object
      `dsl` is re-cunstrcut object
    - `wrapper` is faster to write backend
      `dsl` is use to create tablegen which work with exists file
* Wrapper legacy feature
    - we will remove the feature to create object with 'ClassWrapper'
      You should use `dsl` api instead.

First, RecordContext is a Namespace
```python
ctx = RecordContext()
ctx.load("RISC.td")
```

We can define a class, which we want to create, you need describe the value
of Record.

```python
class Instruction(PyRecord, TDRecord=ctx.Instruction):
    name: str

    def __init__(self, name:str):
        self.name = name
```

```python
ctx.Instruction # is a type[TDRecord], which define like
# type('Instruction', (TDRecord,), )
intr = ctx.Instruction(args) # we will provide a simple verify
intr # is a type of ctx.Instruction, TDRecord so it's read-only
intr.x = value # it will be `let` if it exist
intr.y = value # it will be `declare` + `set value`
intr.z = intr.y # in the record def it's not nessacery, if intr.y is not unknown, it will be value
```

```
intr = Instruction(*args)
intr # it will become an PyRecord
dump_def(intr) # def <name> : cls<>;
dump(intr) # cls<>;
ctx.dump(file)
```