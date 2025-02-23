#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "BindType.h"
#include "BindInit.h"

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

void _InitBindingImpl::_def(pyInitKindEnum &kind) {
  kind.value("IK_First",                BindInit::InitKind::IK_First)
      .value("IK_FirstTypedInit",       BindInit::InitKind::IK_FirstTypedInit)
      .value("IK_BitInit",              BindInit::InitKind::IK_BitInit)
      .value("IK_BitsInit",             BindInit::InitKind::IK_BitsInit)
      .value("IK_DagInit",              BindInit::InitKind::IK_DagInit)
      .value("IK_DefInit",              BindInit::InitKind::IK_DefInit)
      .value("IK_FieldInit",            BindInit::InitKind::IK_FieldInit)
      .value("IK_IntInit",              BindInit::InitKind::IK_IntInit)
      .value("IK_ListInit",             BindInit::InitKind::IK_ListInit)
      .value("IK_FirstOpInit",          BindInit::InitKind::IK_FirstOpInit)
      .value("IK_BinOpInit",            BindInit::InitKind::IK_BinOpInit)
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
      // .value("IK_VarListElementInit",   BindInit::InitKind::IK_VarListElementInit)
      .value("IK_VarBitInit",           BindInit::InitKind::IK_VarBitInit)
      .value("IK_VarDefInit",           BindInit::InitKind::IK_VarDefInit)
      .value("IK_LastTypedInit",        BindInit::InitKind::IK_LastTypedInit)
      .value("IK_UnsetInit",            BindInit::InitKind::IK_UnsetInit)
      //.value("IK_ArgumentInit",         BindInit::InitKind::IK_ArgumentInit)
    ;
}

void _InitBindingImpl::_def(pyBinaryOpEnum &kind) {
  kind.value("ADD", BindBinOpInit::ADD)
      .value("SUB", BindBinOpInit::SUB)
      .value("MUL", BindBinOpInit::MUL)
      //.value("DIV", BindBinOpInit::DIV)
      .value("OR", BindBinOpInit::OR)
      .value("AND", BindBinOpInit::AND)
      .value("XOR", BindBinOpInit::XOR)
      .value("SHL", BindBinOpInit::SHL)
      .value("SRA", BindBinOpInit::SRA)
      .value("SRL", BindBinOpInit::SRL)
      .value("LISTCONCAT", BindBinOpInit::LISTCONCAT)
      //.value("LISTSLICE", BindBinOpInit::LISTSLICE)
      //.value("RANGEC", BindBinOpInit::RANGEC)
      .value("STRCONCAT", BindBinOpInit::STRCONCAT)
      .value("EQ", BindBinOpInit::EQ)
      .value("NE", BindBinOpInit::NE)
      .value("LT", BindBinOpInit::LT)
      .value("LE", BindBinOpInit::LE)
      .value("GT", BindBinOpInit::GT)
      .value("GE", BindBinOpInit::GE)
      //.value("GETDAGARG", BindBinOpInit::GETDAGARG)
      //.value("GETDAGNAME", BindBinOpInit::GETDAGNAME)
      //.value("GETDAGOP", BindBinOpInit::GETDAGOP)
    ;
}

void _InitBindingImpl::_def(pyStringFormatEnum &cls) {
  cls.value("SF_String", StringInit::StringFormat::SF_String)
     .value("SF_Code", StringInit::StringFormat::SF_Code);
}

void _InitBindingImpl::_def(pyInitClass &cls) {
    cls.def("getAsString", &llvm::Init::getAsString)
      .def("isConcrete", &llvm::Init::isConcrete)
      .def("getBit", &llvm::Init::getBit)
      .def("getKind", &llvm::Init::getKind)
    ;
}

void _InitBindingImpl::_def(pyTypedInitClass &cls) {
    cls.def_static("classof", &llvm::TypedInit::classof)
      .def("getType", &llvm::TypedInit::getType, py::return_value_policy::reference)
    ;
}

void _InitBindingImpl::_def(pyUnsetInitClass &cls) {
    cls.def("getAsString", &llvm::UnsetInit::getAsString)
    ;
}

void _InitBindingImpl::_def(pyOpInitClass &cls) {
    cls.def("getNumOperands", &llvm::OpInit::getNumOperands);
}

void _InitBindingImpl::_def(pyBinOpInitClass &cls) {
    cls.def("getOpcode", &llvm::BinOpInit::getOpcode);
    cls.def("getLHS", &llvm::BinOpInit::getLHS, py::return_value_policy::reference);
    cls.def("getRHS", &llvm::BinOpInit::getRHS, py::return_value_policy::reference);
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

void _InitBindingImpl::_def(pyStringInitClass &cls) {
    cls.def("getValue", &BindStringInitImpl::getValue)
      .def("getAsString", &BindStringInitImpl::getAsString)
      .def("getAsUnquotedString", &BindStringInitImpl::getAsUnquotedString)
      .def("isConcrete", &llvm::StringInit::isConcrete)
      .def("getFormat", &llvm::StringInit::getFormat)
    ;
}

void _InitBindingImpl::_def(pyBitInitClass &cls) {
  cls.def("getValue",    &llvm::BitInit::getValue)
     .def("getBit",      &llvm::BitInit::getBit, py::return_value_policy::reference)
     .def("isConcrete",  &llvm::BitInit::isConcrete)
     .def("getAsString", &llvm::BitInit::getAsString)
    ;
}

void  _InitBindingImpl::_def(pyBitsInitClass &cls){
   cls.def("getBit",        &llvm::BitsInit::getBit, py::return_value_policy::reference)
      .def("isConcrete",    &llvm::BitsInit::isConcrete)
      .def("getAsString",   &llvm::BitsInit::getAsString)
      .def("getNumBits",    &llvm::BitsInit::getNumBits)
      .def("isComplete",    &llvm::BitsInit::isComplete)
      .def("allInComplete", &llvm::BitsInit::allInComplete)
    ;
}

void _InitBindingImpl::_def(pyDefInitClass &cls) {
  cls.def("isConcrete",    &llvm::DefInit::isConcrete)
      .def("getAsString",   &llvm::DefInit::getAsString)
      .def("getDef",        &llvm::DefInit::getDef, py::return_value_policy::reference)
    ;
}

void _InitBindingImpl::_def(pyListInitClass &cls) {
  cls.def("getElement",         &llvm::ListInit::getElement)
      .def("getElementType",     &llvm::ListInit::getElementType, py::return_value_policy::reference)
      .def("getElementAsRecord", &llvm::ListInit::getElementAsRecord, py::return_value_policy::reference)
      .def("isConcrete",         &llvm::ListInit::isConcrete)
      .def("getAsString",        &llvm::ListInit::getAsString)
      .def("isComplete",         &llvm::ListInit::isComplete)
      .def("size",               &llvm::ListInit::size)
      .def("empty",              &llvm::ListInit::empty)
      .def("getBit",             &llvm::ListInit::getBit)
      .def("getValues",          [](ListInit &Self){return Self.getValues().vec();})
    ;
}

void _InitBindingImpl::_def(pyIntInitClass &cls) {
  cls.def("getValue",    &llvm::IntInit::getValue)
      .def("getAsString", &llvm::IntInit::getAsString)
      .def("isConcrete",  &llvm::IntInit::isConcrete)
      .def("getBit", &llvm::IntInit::getBit, py::return_value_policy::reference)
    ;
}

void _InitBindingImpl::_def(pyDagInitClass &cls) {
  cls.def("getOperator", &llvm::DagInit::getOperator, py::return_value_policy::reference)
    .def("getName", &llvm::DagInit::getName, py::return_value_policy::reference)
    .def("getNameStr", [](DagInit &Self){return Self.getNameStr().str();})
    .def("getNumArgs", &llvm::DagInit::getNumArgs)
    .def("getArg", &llvm::DagInit::getArg, py::return_value_policy::reference)
    .def("getArgName", &llvm::DagInit::getArgName)
    .def("getArgs", [](DagInit &Self){return Self.getArgs().vec();})
    .def("getArgNames", [](DagInit &Self){return Self.getArgNames().vec();})
    ;
}

void _InitBindingImpl::_def(pyVarInitClass &cls) {
  cls.def("getName", [](VarInit &Self){return Self.getName().str();})
    .def("getNameInit", &llvm::VarInit::getNameInit, py::return_value_policy::reference)
    .def("getNameInitAsString", &llvm::VarInit::getNameInitAsString)
    .def("getAsString", &llvm::VarInit::getAsString)
    ;
}

void _InitBindingImpl::_def(pyVarBitInitClass &cls) {
  cls.def("getBitVar", &llvm::VarBitInit::getBitVar, py::return_value_policy::reference)
     .def("getBitNum", &llvm::VarBitInit::getBitNum)
     .def("getAsString", &llvm::VarBitInit::getAsString)
    ;
}

void def_other_Init(py::module &m) {

    // StringInit
    py::enum_<StringInit::StringFormat>(m, "StringFormat")
      .value("SF_String", StringInit::StringFormat::SF_String)
      .value("SF_Code", StringInit::StringFormat::SF_Code)
    ;
}

