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

using pyRecordKeeperClass = py::class_<llvm::RecordKeeper>;
using pyRecordClass = py::class_<llvm::Record>;
using pySMLocClass = py::class_<SMLoc>;
using pyRecordValClass = py::class_<RecordVal>;
using pySMRangeClass = pybind11::class_<llvm::SMRange>;

struct _RecordBindingImpl {
    pyRecordKeeperClass pyrecordkeepercls;
    pyRecordClass       pyrecordcls;
    pyRecordValClass    pyrecordvalcls;
    pySMLocClass        pysmloccls;
    pySMRangeClass      pysmrangecls;

    _RecordBindingImpl(py::module &m) : 
        pyrecordkeepercls(m, "RecordKeeper"),
        pyrecordcls(m, "Record"),
        pyrecordvalcls(m, "RecordVal"),
        pysmloccls(m, "SMLoc"),
        pysmrangecls(m, "SMRange") {}

    void _def(pyRecordKeeperClass&);
    void _def(pyRecordClass&);
    void _def(pyRecordValClass&);
    void _def(pySMLocClass&);
    void _def(pySMRangeClass&);

    void def() {
        _def(pyrecordkeepercls);
        _def(pyrecordcls);
        _def(pyrecordvalcls);
        _def(pysmloccls);
        _def(pysmrangecls);
    }
};