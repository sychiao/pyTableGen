from tablegen.wrapper.recordkeeper import RecordKeeper
import tablegen
import textwrap
import os

llvm_path = tablegen.binding.getLLVMSourceLoc()
incDir = os.path.join(llvm_path, 'include')
TargetDir = os.path.join(llvm_path, 'lib', 'Target', 'RISCV')
riscv_td = os.path.join(TargetDir, 'RISCV.td')

RK = RecordKeeper.load(riscv_td, [incDir, TargetDir])

def printTableGenClass(B):
    stmts = []
    args = ["self"]
    print(f"class {B.defname}({', '.join(B.bases) if B.bases else "TableGenRecord"}):")
    
    for k, v in B.fields.items():
        if ":" in k:
            clsname, name = k.split(":", 1)
            args.append(f"{name}: {v.__name__} = {repr(B[k])}")
        else:
            stmts.append(f"self.{k}: {v.__name__} = {repr(B[k])}")
        B[k]
    print(f"  def __init__({', '.join(args)}):")
    print(textwrap.indent("\n".join(stmts), '    '))

for name,cls in RK.getClasses().items():
    if cls:
        printTableGenClass(cls)