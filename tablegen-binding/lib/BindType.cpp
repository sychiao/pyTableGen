#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"
#include "BindType.h"

namespace py = pybind11;
using namespace llvm;


void def_Type(py::module& m) {
    py::bind_vector<std::vector<std::string>>(m, "StringVector");
    py::implicitly_convertible<py::iterable, std::vector<std::string>>();
    py::bind_vector<RecordVector>(m, "RecordVector");
    py::bind_vector<RecordValVector>(m, "RecordValVector");
    py::bind_vector<SMLocVector>(m, "SMLocVector");
    py::bind_map<RecordMap>(m, "RecordMap");
    py::bind_vector<InitVector>(m, "InitVector");
    py::bind_vector<StringInitVector>(m, "StringInitVector");
    py::bind_vector<SuperClassVector>(m, "SuperClassVector");
}