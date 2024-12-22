#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"

namespace py = pybind11;
using namespace llvm;

using pyRecTyKindEnum = py::enum_<RecTy::RecTyKind>;
using pyRecTyClass = py::class_<RecTy>;
using pyBitRecTyClass = py::class_<BitRecTy, RecTy>;
using pyBitsRecTyClass = py::class_<BitsRecTy, RecTy>;
using pyDagRecTyClass = py::class_<DagRecTy, RecTy>;
using pyIntRecTyClass = py::class_<IntRecTy, RecTy>;
using pyListRecTyClass = py::class_<ListRecTy, RecTy>;
using pyRecordRecTyClass = py::class_<RecordRecTy, RecTy>;
using pyStringRecTyClass = py::class_<StringRecTy, RecTy>;

struct _RecTyBindingImpl {
  pyRecTyKindEnum recTyKindEnum;
  pyRecTyClass recTycls;
  pyBitRecTyClass bitrecTycls;
  pyBitsRecTyClass bitsrecTycls;
  pyDagRecTyClass dagrecTycls;
  pyIntRecTyClass intrecTycls;
  pyListRecTyClass listrecTycls;
  pyRecordRecTyClass recordrecTycls;
  pyStringRecTyClass stringtycls;

  _RecTyBindingImpl(py::module &m) : 
    recTyKindEnum(m, "RecTyKind"),
    recTycls(m, "RecTy"),
    bitrecTycls(m, "BitRecTy"),
    bitsrecTycls(m, "BitsRecTy"),
    dagrecTycls(m, "DagRecTy"),
    intrecTycls(m, "IntRecTy"),
    listrecTycls(m, "ListRecTy"),
    recordrecTycls(m, "RecordRecTy"),
    stringtycls(m, "StringRecTy"){}

    void _def(pyRecTyKindEnum &) ;
    void _def(pyRecTyClass &);
    void _def(pyBitRecTyClass &);
    void _def(pyBitsRecTyClass &cls);
    void _def(pyStringRecTyClass &);
    void _def(pyDagRecTyClass &);
    void _def(pyIntRecTyClass &);
    void _def(pyListRecTyClass &);
    void _def(pyRecordRecTyClass &);

    void def() {
        _def(recTyKindEnum);
        _def(recTycls);
        _def(bitrecTycls);
        _def(bitsrecTycls);
        _def(dagrecTycls);
        _def(intrecTycls);
        _def(listrecTycls);
        _def(recordrecTycls);
        _def(stringtycls);
    }
};

void def_RecordRecTy(py::module &m, pyRecordRecTyClass &);
