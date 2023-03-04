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

using StringVector = std::vector<std::string>;
using RecordVector = std::vector<Record*>;
using RecordValVector = std::vector<RecordVal>;
using InitVector = std::vector<Init*>;
using RecordMap = std::map<std::string, Record*, std::less<>>;
using SMLocVector = std::vector<SMLoc>;

PYBIND11_MAKE_OPAQUE(RecordVector)
PYBIND11_MAKE_OPAQUE(RecordValVector)
PYBIND11_MAKE_OPAQUE(StringVector)
PYBIND11_MAKE_OPAQUE(RecordMap)
PYBIND11_MAKE_OPAQUE(InitVector)
PYBIND11_MAKE_OPAQUE(SMLocVector)


void def_Type(py::module& m) {
    py::bind_vector<std::vector<std::string>>(m, "StringVector");
    py::implicitly_convertible<py::iterable, std::vector<std::string>>();

    py::bind_vector<RecordVector>(m, "RecordVector");
    py::bind_vector<RecordValVector>(m, "RecordValVector");
    py::bind_vector<InitVector>(m, "InitVector");
    py::bind_vector<SMLocVector>(m, "SMLocVector");
    py::bind_map<RecordMap>(m, "RecordMap");
}