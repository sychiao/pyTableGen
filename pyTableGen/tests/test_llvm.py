import sys
import os

source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(source_path, '..', 'src'))
print("PATH:", os.path.join(source_path, '..', 'src'))

#from tablegen.Context import TableGenLoader
#from tablegen.RecTy.type import TableGenType
import tablegen.binding as binding

from tablegen.unit.record import TypedRecord
from tablegen.context import TableGenContext

llvm_path = binding.getLLVMSourceLoc()
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')
#print(riscv_td)
#ctx = TableGenLoader().load(riscv_td, [incDir, TargetDir])

Recs = binding.ParseTableGen(riscv_td, [incDir, TargetDir])

from dataclasses import dataclass

class ValueType(TypedRecord):
    Namespace: str
    Size: int
    Value: int


@dataclass
class RegisterClass(TypedRecord):
    Namespace: str
    RegTypes: list[ValueType]
    Size: int

    def area(self):
        return self.Size * len(self.RegTypes)

#for rec in Recs.getAllDerivedDefinitions(RegisterClass.__name__):
#    print(RegisterClass(rec).Size)
#    print(RegisterClass(rec).RegTypes)
#    print(RegisterClass(rec).Namespace)

import time
a = time.time()
Recs = binding.ParseTableGen(riscv_td, [incDir, TargetDir])

rec = Recs.getClass("RegisterClass")
print(">> rec", rec)
for recVal in rec.getValues():
    print(">> recVal", recVal.getName(), recVal.getType().getAsString(), recVal.getValue().getAsString(), recVal.isTemplateArg())

'''
exit()

s = time.time()
ctx = TableGenContext(Recs)
for rec in ctx.getDefs(RegisterClass):
    print(rec.Size)

x = time.time()

for rec in ctx.getDefs("RegisterClass"):
    rec.__late_init__()
e = time.time()
for rec in ctx.getDefs(RegisterClass):
    rec.__late_init__()
m2 = time.time()
for r in ctx.getDefs("RegisterClass"):
    r.__late_init__()
e2 = time.time()

for rec in ctx.getDefs(RegisterClass):
    print("***", rec.recname, rec.area())

sz = len(list(ctx.getDefs(RegisterClass)))
print(f"Total parse file use {s-a} sec")
print(f"  create {sz} object 1  use {x-s} sec (avg. {(x-s)/sz})")
print(f"  create {sz} object 2(cached)  use {e-x} sec (avg. {(e-x)/sz})")
print(f"  late_init TypedRecord(Partial) {sz} object use {m2-e} sec (avg. {(m2-e)/sz})")
print(f"  late_init TableRecord(Full)    {sz} object use {e2-m2} sec (avg. {(e2-m2)/sz})")

#import pickle
#with open("riscv_td.pkl", "wb") as f:
#    pickle.dump(ctx, f)
'''