import sys
import os

source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(source_path, '..', 'src'))
print("PATH:", os.path.join(source_path, '..', 'src'))

from tablegen.Context import TableGenLoader

llvm_path = os.path.join(source_path, '..', '..', '..', 'llvm')
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')
print(riscv_td)
ctx = TableGenLoader().load(riscv_td, [incDir, TargetDir])

import pickle
with open("riscv_td.pkl", "wb") as f:
    pickle.dump(ctx, f)