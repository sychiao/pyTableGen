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
#include "BindRecTy.h"
#include <iostream>

namespace py = pybind11;
using namespace llvm;

struct BindRecordRecTyImpl {
  static std::vector<Record*> getClasses(RecordRecTy &Self) {
    return Self.getClasses().vec();
  }
};

void _RecTyBindingImpl::_def(pyRecTyKindEnum &cls) {
  cls.value("BitRecTyKind",    RecTy::RecTyKind::BitRecTyKind)
     .value("BitsRecTyKind",   RecTy::RecTyKind::BitsRecTyKind)
     .value("IntRecTyKind",    RecTy::RecTyKind::IntRecTyKind)
     .value("StringRecTyKind", RecTy::RecTyKind::StringRecTyKind)
     .value("ListRecTyKind",   RecTy::RecTyKind::ListRecTyKind)
     .value("DagRecTyKind",    RecTy::RecTyKind::DagRecTyKind)
     .value("RecordRecTyKind", RecTy::RecTyKind::RecordRecTyKind)
  ;
}

void _RecTyBindingImpl::_def(pyRecTyClass &cls) {
  cls.def("getRecTyKind", &llvm::RecTy::getRecTyKind)
    .def("getRecordKeeper", &llvm::RecTy::getRecordKeeper)
    .def("getAsString",  &llvm::RecTy::getAsString)
    .def("typeIsConvertibleTo", &llvm::RecTy::typeIsConvertibleTo)
    .def("typeIsA", &llvm::RecTy::typeIsA);
}

void _RecTyBindingImpl::_def(pyBitRecTyClass &cls) {
  cls.def("getAsString", &llvm::BitRecTy::getAsString)
     .def("typeIsConvertibleTo", &llvm::BitRecTy::typeIsConvertibleTo)
    ;
}

void _RecTyBindingImpl::_def(pyBitsRecTyClass &cls) {
  cls.def("getAsString", &llvm::BitsRecTy::getAsString)
     .def("getNumBits", &llvm::BitsRecTy::getNumBits)
     .def("typeIsConvertibleTo", &llvm::BitsRecTy::typeIsConvertibleTo)
    ;
}

void _RecTyBindingImpl::_def(pyDagRecTyClass &cls) {
  cls.def("getAsString", &llvm::DagRecTy::getAsString);
}

void _RecTyBindingImpl::_def(pyIntRecTyClass &cls) {
  cls.def("getAsString", &llvm::IntRecTy::getAsString)
     .def("typeIsConvertibleTo", &llvm::IntRecTy::typeIsConvertibleTo)
    ;
}

void _RecTyBindingImpl::_def(pyListRecTyClass &cls) {
  cls.def("getAsString", &llvm::ListRecTy::getAsString)
     .def("getElementType", &llvm::ListRecTy::getElementType, py::return_value_policy::reference)
     .def("typeIsA",  &llvm::ListRecTy::typeIsA)
     .def("typeIsConvertibleTo", &llvm::ListRecTy::typeIsConvertibleTo)
    ;
}

void _RecTyBindingImpl::_def(pyRecordRecTyClass &cls) {
  cls.def("getClasses", &BindRecordRecTyImpl::getClasses)
     .def("getAsString", &llvm::RecordRecTy::getAsString)
     .def("isSubClassOf", &llvm::RecordRecTy::isSubClassOf)
     .def("typeIsA", &llvm::RecordRecTy::typeIsA)
     .def("typeIsConvertibleTo", &llvm::RecordRecTy::typeIsConvertibleTo)
    ;
}

void _RecTyBindingImpl::_def(pyStringRecTyClass &cls) {
  cls.def("getAsString", &llvm::StringRecTy::getAsString)
     .def("typeIsConvertibleTo", &llvm::StringRecTy::typeIsConvertibleTo)
    ;
}



