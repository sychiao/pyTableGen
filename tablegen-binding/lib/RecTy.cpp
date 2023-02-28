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


struct BindRecordRecTyImpl {
  static std::vector<Record*> getClasses(RecordRecTy &Self) {
    return Self.getClasses().vec();
  }
};


void def_RecTy(py::module &m) {
  py::enum_<RecTy::RecTyKind>(m, "RecTyKind")
      .value("BitRecTyKind",    RecTy::RecTyKind::BitRecTyKind)
      .value("BitsRecTyKind",   RecTy::RecTyKind::BitsRecTyKind)
      .value("IntRecTyKind",    RecTy::RecTyKind::IntRecTyKind)
      .value("StringRecTyKind", RecTy::RecTyKind::StringRecTyKind)
      .value("ListRecTyKind",   RecTy::RecTyKind::ListRecTyKind)
      .value("DagRecTyKind",    RecTy::RecTyKind::DagRecTyKind)
      .value("RecordRecTyKind", RecTy::RecTyKind::RecordRecTyKind)
  ;

  py::class_<RecTy>(m, "RecTy")
    .def("getRecTyKind", &llvm::RecTy::getRecTyKind)
    .def("getRecordKeeper", &llvm::RecTy::getRecordKeeper)
    .def("getAsString",  &llvm::RecTy::getAsString)
    .def("typeIsConvertibleTo", &llvm::RecTy::typeIsConvertibleTo)
    .def("typeIsA", &llvm::RecTy::typeIsA)
    // ListRecTy * 	getListTy ()
    ;  

  // RecordRecTy
  py::class_<RecordRecTy, RecTy>(m, "RecordRecTy")
    .def("getClasses", &BindRecordRecTyImpl::getClasses)
    .def("getAsString", &llvm::RecordRecTy::getAsString)
    .def("isSubClassOf", &llvm::RecordRecTy::isSubClassOf)
    ;  
}



