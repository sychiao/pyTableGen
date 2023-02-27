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


TypedInit* casInit2TypedInit(Init* init) {
  return llvm::dyn_cast<TypedInit, Init>(init);
}

struct BindStringInitImpl {
  static std::string getValue(StringInit &Self) {
    return Self.getValue().str();
  }

  static std::string getAsString(StringInit &Self) {
    return Self.getAsString();
  }

  static std::string getAsUnquotedString(StringInit &Self) {
    return Self.getAsUnquotedString();
  }

};

void def_Init(py::module &m) {
     py::class_<Init>(m, "Init")
      .def("getAsString", &llvm::Init::getAsString);

    // TypedInit
    py::class_<TypedInit, Init>(m, "TypedInit")
      .def_static("cast", &casInit2TypedInit)
      .def_static("classof", &llvm::TypedInit::classof)
    ;

    // IntInit
    py::class_<IntInit, TypedInit>(m, "IntInit")
      .def("getValue",    &llvm::IntInit::getValue)
      .def("getAsString", &llvm::IntInit::getAsString)
      .def("isConcrete",  &llvm::IntInit::isConcrete)
    ;

    // StringInit
    py::enum_<StringInit::StringFormat>(m, "StringFormat")
      .value("SF_String", StringInit::StringFormat::SF_String)
      .value("SF_Code", StringInit::StringFormat::SF_Code)
    ;

    py::class_<StringInit, TypedInit>(m, "StringInit")
      .def("getValue", &BindStringInitImpl::getValue)
      .def("getAsString", &BindStringInitImpl::getAsString)
      .def("getFormat", &llvm::StringInit::getFormat)
      .def("getAsUnquotedString", &BindStringInitImpl::getAsUnquotedString)
      .def("isConcrete", &llvm::StringInit::isConcrete)
    ;
}