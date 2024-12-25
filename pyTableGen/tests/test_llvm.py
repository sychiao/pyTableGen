import sys
import os

source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(source_path, '..', 'src'))
print("PATH:", os.path.join(source_path, '..', 'src'))

from tablegen.Context import TableGenLoader
from tablegen.RecTy.type import TableGenType
import tablegen.binding as binding

from tablegen.RecTy.type import TableGenRecord, TableGenContext


llvm_path = os.path.join(source_path, '..', '..', '..', 'llvm')
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')
#print(riscv_td)
#ctx = TableGenLoader().load(riscv_td, [incDir, TargetDir])

Recs = binding.ParseTableGen(riscv_td, [incDir, TargetDir])

class ValueType(TableGenType):
    Namespace: str
    Size: int
    Value: int

class RegisterClass(TableGenType):
    Namespace: str
    RegTypes: list[ValueType]
    Size: int

#for rec in Recs.getAllDerivedDefinitions(RegisterClass.__name__):
#    print(RegisterClass(rec).Size)
#    print(RegisterClass(rec).RegTypes)
#    print(RegisterClass(rec).Namespace)

import time
a = time.time()
Recs = binding.ParseTableGen(riscv_td, [incDir, TargetDir])
s = time.time()
ctx = TableGenContext()
lst = list()
for _, rec in Recs.getDefs().items():
    lst.append(TableGenRecord(rec, ctx))
e = time.time()

for r in lst:
    r.__late_init__()

e2 = time.time()

sz = len(Recs.getDefs())
print(f"Total parse file use {s-a} sec")
print(f"  create {sz} object  use {e-s} sec (avg. {(e-s)/sz})")
print(f"  late_init {sz} object use {e2-e} sec (avg. {(e2-e)/sz})")

#import pickle
#with open("riscv_td.pkl", "wb") as f:
#    pickle.dump(ctx, f)