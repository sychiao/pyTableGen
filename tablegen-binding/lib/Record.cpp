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
      .def("getNameInit", [](RecordVal &Self){return Self.getNameInit(); }, py::return_value_policy::reference)
      .def("getValue", [](RecordVal &Self){return Self.getValue(); }, py::return_value_policy::reference)
    ;  
}

struct BindRecordImpl {
  static std::vector<RecordVal> getValues(Record &Self) {
    return Self.getValues().vec();
  }

  static std::vector<Init*> getTemplateArgs(Record &Self) {
    return Self.getTemplateArgs().vec();
  }

  static std::vector<SMLoc> getLoc(Record &Self) {
    return Self.getLoc().vec();
  }

  static std::vector<SMLoc> getForwardDeclarationLocs(Record &Self) {
    return Self.getForwardDeclarationLocs().vec();
  }

  static RecordVal* getValue(Record &Self, std::string name) {
    return Self.getValue(name);
  }

  static RecordVal* getValue(Record &Self, Init *name) {
    return Self.getValue(name);
  }

  static bool isSubClassOf (Record &Self, Record &R) {
    return Self.isSubClassOf(&R);
  }

  static bool isSubClassOf (Record &Self, std::string name) {
    return Self.isSubClassOf(name);
  }

};

void def_Record(py::module &m) {
    py::class_<llvm::SMLoc>(m, "SMLoc")
      .def("isValid", &llvm::SMLoc::isValid)
      .def("getPointer", &llvm::SMLoc::getPointer);

    py::class_<llvm::Record>(m, "Record")
      .def("getID", [](Record &Self) {return Self.getID();})
      .def("getNameInit", [](Record &Self) {return Self.getNameInit();}, py::return_value_policy::reference)
      .def("getDefInit",  [](Record &Self) {return Self.getDefInit();}, py::return_value_policy::reference)
      .def("getName", [](Record &Self) {return Self.getName().str();})
      .def("getValues", &BindRecordImpl::getValues)
      .def("getLoc", *BindRecordImpl::getLoc)    
      .def("getForwardDeclarationLocs", *BindRecordImpl::getForwardDeclarationLocs)
      .def("getTemplateArgs", &BindRecordImpl::getTemplateArgs)
      .def("isTemplateArg", &Record::isTemplateArg)
      .def("getType", &llvm::Record::getType, py::return_value_policy::reference)
      .def("getRecords", &llvm::Record::getRecords)
      .def("isAnonymous", &llvm::Record::isAnonymous)
      .def("getValueInit", &llvm::Record::getValueInit, py::return_value_policy::reference)
      .def("getValue", py::overload_cast<Record&, std::string>(&BindRecordImpl::getValue), py::return_value_policy::reference)
      .def("isValueUnset", [](Record &Self, std::string FieldName){return Self.isValueUnset(FieldName);})
      .def("isSubClassOf", py::overload_cast<Record&, Record&>(&BindRecordImpl::isSubClassOf))
      .def("isSubClassOf", py::overload_cast<Record&, std::string>(&BindRecordImpl::isSubClassOf))
      .def("getFieldLoc", [](Record &Self, std::string FieldName){return Self.getFieldLoc(FieldName);})
      .def("getValueAsString", [](Record &Self, std::string FieldName){return Self.getValueAsString(FieldName).str();})
      .def("getValueAsBitsInit", [](Record &Self, std::string FieldName){return Self.getValueAsBitsInit(FieldName);})
      .def("getValueAsListInit", [](Record &Self, std::string FieldName){return Self.getValueAsListInit(FieldName);})
      .def_property_readonly("isClass", &Record::isClass)
    ;
}


