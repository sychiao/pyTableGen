#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"

namespace py = pybind11;
using namespace llvm;

using StringVector = std::vector<std::string>;
using RecordVector = std::vector<Record*>;
using RecordValVector = std::vector<RecordVal>;
using InitVector = std::vector<Init*>;
using StringInitVector = std::vector<StringInit*>;
using RecordMap = std::map<std::string, Record*, std::less<>>;
using SMLocVector = std::vector<SMLoc>;

PYBIND11_MAKE_OPAQUE(RecordVector)
PYBIND11_MAKE_OPAQUE(RecordValVector)
PYBIND11_MAKE_OPAQUE(StringVector)
PYBIND11_MAKE_OPAQUE(RecordMap)
PYBIND11_MAKE_OPAQUE(SMLocVector)
PYBIND11_MAKE_OPAQUE(InitVector)
PYBIND11_MAKE_OPAQUE(StringInitVector)

using pyRecordKeeperClass = py::class_<llvm::RecordKeeper>;
using pyRecordClass = py::class_<llvm::Record>;
using pySMLocClass = py::class_<SMLoc>;
using pyRecordValClass = py::class_<RecordVal>;
using pyRecTyKindEnum = py::enum_<RecTy::RecTyKind>;
using pyRecTyClass = py::class_<RecTy>;
using pyRecordRecTyClass = py::class_<RecordRecTy, RecTy>;

void def_RecordKeeper(pyRecordKeeperClass &);
void def_SMLoc(pySMLocClass &);
void def_Record(pyRecordClass &);
void def_RecordVal(pyRecordValClass &);
void def_RecTy(pyRecTyClass &);
void def_RecTyKind(pyRecTyKindEnum &);
void def_RecordRecTy(py::module &m, pyRecordRecTyClass &);

void def_Type(py::module& m);
using pyInitClass = py::class_<Init>;
using pyTypedInitClass = py::class_<TypedInit, Init>;
using pyOpInitClass = py::class_<OpInit, TypedInit>;
using pyBinOpInitClass = py::class_<BinOpInit, OpInit>;
using pyStringInitClass = pybind11::class_<llvm::StringInit, llvm::TypedInit>;

void def_InitKind(py::module &m);
void def_other_Init(py::module &m);

void def_Init(pyInitClass &cls);
void def_StringInit(pyInitClass &);
void def_TypedInit(pyTypedInitClass &);
void def_OpInit(pyOpInitClass &);
void def_BinOpInit(pyBinOpInitClass &);
void def_StringInit(pyStringInitClass &);
