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
#include <iostream>

namespace py = pybind11;
using namespace llvm;


struct BindRecordRecTyImpl {
  static std::vector<Record*> getClasses(RecordRecTy &Self) {
    return Self.getClasses().vec();
  }
};

void def_RecTyKind(pyRecTyKindEnum &cls) {
  cls.value("BitRecTyKind",    RecTy::RecTyKind::BitRecTyKind)
     .value("BitsRecTyKind",   RecTy::RecTyKind::BitsRecTyKind)
     .value("IntRecTyKind",    RecTy::RecTyKind::IntRecTyKind)
     .value("StringRecTyKind", RecTy::RecTyKind::StringRecTyKind)
     .value("ListRecTyKind",   RecTy::RecTyKind::ListRecTyKind)
     .value("DagRecTyKind",    RecTy::RecTyKind::DagRecTyKind)
     .value("RecordRecTyKind", RecTy::RecTyKind::RecordRecTyKind)
  ;
}


void def_RecTy(pyRecTyClass &cls) {
   cls.def("getRecTyKind", &llvm::RecTy::getRecTyKind)
    .def("getRecordKeeper", &llvm::RecTy::getRecordKeeper)
    .def("getAsString",  &llvm::RecTy::getAsString)
    .def("typeIsConvertibleTo", &llvm::RecTy::typeIsConvertibleTo)
    .def("typeIsA", &llvm::RecTy::typeIsA)
    // ListRecTy * 	getListTy ()
    ;
  // RecordRecTy
}

void def_RecordRecTy(py::module &m, pyRecordRecTyClass &cls) {
  cls.def("getClasses", &BindRecordRecTyImpl::getClasses)
     .def("getAsString", &llvm::RecordRecTy::getAsString)
     .def("isSubClassOf", &llvm::RecordRecTy::isSubClassOf)
     .def("typeIsA", &llvm::RecordRecTy::typeIsA)
     .def("typeIsConvertibleTo", &llvm::RecordRecTy::typeIsConvertibleTo)
    ;

  py::class_<StringRecTy, RecTy>(m, "StringRecTy")
    .def("getAsString", &llvm::StringRecTy::getAsString)
    .def("typeIsConvertibleTo", &llvm::StringRecTy::typeIsConvertibleTo)
    ;

}



