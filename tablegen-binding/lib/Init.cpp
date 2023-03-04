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

class BindInit : public Init { // helper type for exposing protected functions
public:
    using Init::InitKind; // inherited with different access modifier
};

void def_Init(py::module &m) {
     // InitKind
     py::enum_<BindInit::InitKind>(m, "InitKind")
      .value("IK_First",                BindInit::InitKind::IK_First)
      .value("IK_FirstTypedInit",       BindInit::InitKind::IK_FirstTypedInit)
      .value("IK_BitInit",              BindInit::InitKind::IK_BitInit)
      .value("IK_BitsInit",             BindInit::InitKind::IK_FirstTypedInit)
      .value("IK_DagInit",              BindInit::InitKind::IK_BitsInit)
      .value("IK_DefInit",              BindInit::InitKind::IK_DefInit)
      .value("IK_IntInit",              BindInit::InitKind::IK_IntInit)
      .value("IK_ListInit",             BindInit::InitKind::IK_ListInit)
      .value("IK_FirstOpInit",          BindInit::InitKind::IK_FirstOpInit)
      .value("IK_TernOpInit",           BindInit::InitKind::IK_TernOpInit)
      .value("IK_UnOpInit",             BindInit::InitKind::IK_UnOpInit)
      .value("IK_LastOpInit",           BindInit::InitKind::IK_LastOpInit)
      .value("IK_CondOpInit",           BindInit::InitKind::IK_CondOpInit)
      .value("IK_FoldOpInit",           BindInit::InitKind::IK_FoldOpInit)
      .value("IK_IsAOpInit",            BindInit::InitKind::IK_IsAOpInit)
      .value("IK_ExistsOpInit",         BindInit::InitKind::IK_ExistsOpInit)
      .value("IK_AnonymousNameInit",    BindInit::InitKind::IK_AnonymousNameInit)
      .value("IK_StringInit",           BindInit::InitKind::IK_StringInit)
      .value("IK_VarInit",              BindInit::InitKind::IK_VarInit)
      .value("IK_VarListElementInit",   BindInit::InitKind::IK_VarListElementInit)
      .value("IK_VarBitInit",           BindInit::InitKind::IK_VarBitInit)
      .value("IK_VarDefInit",           BindInit::InitKind::IK_VarDefInit)
      .value("IK_LastTypedInit",        BindInit::InitKind::IK_LastTypedInit)
      .value("IK_UnsetInit",            BindInit::InitKind::IK_UnsetInit)
    ;

    py::class_<Init>(m, "Init")
      .def("getKind", &llvm::Init::getKind)
      .def("getAsString", &llvm::Init::getAsString);

    // TypedInit
    py::class_<TypedInit, Init>(m, "TypedInit")
      .def_static("cast", &casInit2TypedInit)
      .def_static("classof", &llvm::TypedInit::classof)
    ;

    // BitInit
    py::class_<BitInit, TypedInit>(m, "BitInit")
      .def("getValue",    &llvm::BitInit::getValue)
      .def("getBit",      &llvm::BitInit::getBit)
      .def("isConcrete",  &llvm::BitInit::isConcrete)
      .def("getAsString", &llvm::BitInit::getAsString)
    ;

    // BitsInit
    py::class_<BitsInit, TypedInit>(m, "BitsInit")
      .def("getBit",        &llvm::BitsInit::getBit)
      .def("isConcrete",    &llvm::BitsInit::isConcrete)
      .def("getAsString",   &llvm::BitsInit::getAsString)
      .def("getNumBits",    &llvm::BitsInit::getNumBits)
      .def("isComplete",    &llvm::BitsInit::isComplete)
      .def("allInComplete", &llvm::BitsInit::allInComplete)
    ;

    // DefInit
    py::class_<DefInit, TypedInit>(m, "DefInit")
      .def("isConcrete",    &llvm::DefInit::isConcrete)
      .def("getAsString",   &llvm::DefInit::getAsString)
      .def("getDef",        &llvm::DefInit::getDef)
    ;

    // ListInit 
    py::class_<ListInit, TypedInit>(m, "ListInit")
      .def("getElement",    &llvm::ListInit::getElement)
      .def("isConcrete",    &llvm::ListInit::isConcrete)
      .def("getAsString",   &llvm::ListInit::getAsString)
      .def("isComplete",    &llvm::ListInit::isComplete)
      .def("size",          &llvm::ListInit::size)
      .def("empty",         &llvm::ListInit::empty)
      .def("getBit",        &llvm::ListInit::getBit)
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

    // VarInit
    py::class_<VarInit, TypedInit>(m, "VarInit")
      .def("getName", [](VarInit &Self){return Self.getName().str();})
      .def("getNameInit", &llvm::VarInit::getNameInit)
      .def("getNameInitAsString", &llvm::VarInit::getNameInitAsString)
      .def("getAsString", &llvm::VarInit::getAsString)
    ;

}