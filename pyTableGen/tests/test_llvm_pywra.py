import functools
import sys
import os
from typing import DefaultDict, Iterable
from tablegen.wrapper.recordkeeper import RecordKeeper
import tablegen.binding as binding
from tablegen.unit.dag import DAG, Node
from tablegen.unit.record import TableGenRecord
from tablegen.llvm.RegisterClass import CodeGenRegister

#source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#sys.path.append(os.path.join(source_path, '..', 'src'))
#print("PATH:", os.path.join(source_path, '..', 'src'))

llvm_path = binding.getLLVMSourceLoc()
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')

print("Load TableGen file:", riscv_td)
recs = RecordKeeper.load(riscv_td, [incDir, TargetDir])

dict_name = dict()
from functools import lru_cache

s = CodeGenRegister(recs).getSubRegisterClass(recs.GPR)
print(s)

for value, ty in recs.getClass("RegisterClass").args().items():
    print(value, ty)

print(recs.getClass("RegisterClass"))

RegisterClass = recs.getClass("RegisterClass")

x = RegisterClass("GPR", recs).let("SuperRegClass", recs.getClass("RegisterClass"))