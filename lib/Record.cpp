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

struct RecordKeeper_Impl {
  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, py::args args) {
        auto clsnames = args.cast<std::vector<std::string>>();
        return RecordKeeper_Impl::getAllDerivedDefinitions(Self, clsnames);
  }

  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, std::string clsname) {
        return Self.getAllDerivedDefinitions(clsname);
  }

  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, std::vector<std::string> &clsnames) {
        auto castVec = std::vector<StringRef>(clsnames.begin(), clsnames.end());
        return Self.getAllDerivedDefinitions(	ArrayRef<StringRef>(castVec.data(), castVec.size()));
  }
};

void init_RecordKeeper(py::module &m) {
    //py::bind_map<std::map<std::string, Record*>>(m, "RecordMap");

    py::class_<llvm::RecordKeeper>(m, "RecordKeeper")
      .def(py::init<>())
      .def("getClass", [](llvm::RecordKeeper &Self, std::string clsname) {
            return Self.getClass(clsname);
        }, py::return_value_policy::reference)
      .def("getDef", [](llvm::RecordKeeper &Self, std::string clsname){
            return Self.getDef(clsname);
        }, py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, std::string> (&RecordKeeper_Impl::getAllDerivedDefinitions),
        py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, std::vector<std::string>&> (&RecordKeeper_Impl::getAllDerivedDefinitions),
        py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, py::args> (&RecordKeeper_Impl::getAllDerivedDefinitions), 
        py::return_value_policy::reference)
    ;
}

struct BindRecordImpl {
  static std::vector<RecordVal> getValues(Record &Self) {
    return Self.getValues().vec();
  }
};


void init_Record(py::module &m) {
    py::class_<llvm::Record>(m, "Record")
      .def("getName", [](Record &Self) {return Self.getName().str();})
      .def("getValues", &BindRecordImpl::getValues)
      .def_property_readonly("isClass", &Record::isClass)
    ;

    
}

void init_RecordVal(py::module &m) {
  py::class_<RecordVal>(m, "RecordVal")
      .def("getName", [](RecordVal &Self) {return Self.getName().str();})
      .def("getTypeName", [](RecordVal &Self){return Self.getType()->getAsString(); })
    ;  
}