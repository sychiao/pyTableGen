import os
import tablegen.binding as binding
import tablegen.wrapper.recordkeeper as RK
from tablegen.dsl.context import RecordContext

#source_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
#sys.path.append(os.path.join(source_path, '..', 'src'))
#print("PATH:", os.path.join(source_path, '..', 'src'))

llvm_path = binding.getLLVMSourceLoc()
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')

Recs = RK.RecordKeeper.load(riscv_td, [incDir, TargetDir])
ctx = RecordContext.load(Recs, lazy=True)
print(ctx.Instruction)