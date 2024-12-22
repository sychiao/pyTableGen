import os
import sys

pytbl_root = os.path.join(os.path.dirname(__file__), '..', '..', '..')
binding_root = os.path.join(pytbl_root, 'pyTableGen', 'src')
llvm_root = os.path.join(pytbl_root, '..', '..')
import tablegen.binding

def test_llvm_registerinfo():
    pass