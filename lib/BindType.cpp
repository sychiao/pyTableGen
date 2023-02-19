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

PYBIND11_MAKE_OPAQUE(std::vector<Record*>);
PYBIND11_MAKE_OPAQUE(std::vector<RecordVal>);
PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

void init_Type(py::module& m) {
    py::bind_vector<std::vector<std::string>>(m, "StringVector");
    py::implicitly_convertible<py::iterable, std::vector<std::string>>();

    py::bind_vector<std::vector<Record*>>(m, "RecordVector");
    py::bind_vector<std::vector<RecordVal>>(m, "RecordValVector");
}