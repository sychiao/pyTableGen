#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"

#include <iostream>

namespace py = pybind11;
using namespace llvm;

void def_RecordVal(py::module &m) {
  py::class_<RecordVal>(m, "RecordVal")
      .def("getName", [](RecordVal &Self) {return Self.getName().str();})
      .def("getTypeName", [](RecordVal &Self){return Self.getType()->getAsString(); })
    ;  
}

struct BindRecordImpl {
  static std::vector<RecordVal> getValues(Record &Self) {
    return Self.getValues().vec();
  }
};

void def_Record(py::module &m) {
    py::class_<llvm::Record>(m, "Record")
      .def("getID", [](Record &Self) {return Self.getID();})
      .def("getNameInit", [](Record &Self) {return Self.getNameInit();}, py::return_value_policy::reference)
      .def("getDefInit",  [](Record &Self) {return Self.getDefInit();}, py::return_value_policy::reference)
      .def("getName", [](Record &Self) {return Self.getName().str();})
      .def("getValues", &BindRecordImpl::getValues)
      .def("getType", &llvm::Record::getType, py::return_value_policy::reference)
      .def_property_readonly("isClass", &Record::isClass)
    ;
}


