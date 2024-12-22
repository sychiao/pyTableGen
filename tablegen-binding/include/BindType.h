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
using SuperClassVector = std::vector<std::pair<Record*, SMRange>>;

PYBIND11_MAKE_OPAQUE(RecordVector)
PYBIND11_MAKE_OPAQUE(RecordValVector)
PYBIND11_MAKE_OPAQUE(StringVector)
PYBIND11_MAKE_OPAQUE(RecordMap)
PYBIND11_MAKE_OPAQUE(SMLocVector)
PYBIND11_MAKE_OPAQUE(InitVector)
PYBIND11_MAKE_OPAQUE(StringInitVector)
PYBIND11_MAKE_OPAQUE(SuperClassVector)



