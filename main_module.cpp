#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"

#include "TGParser.h"

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;
using namespace llvm;

RecordKeeper* ParseTableGen(std::string InputFileName) {
    RecordKeeper* records = new RecordKeeper();
    auto srcMgr = SourceMgr();
    ErrorOr<std::unique_ptr<MemoryBuffer>> FileOrErr 
        = MemoryBuffer::getFile(InputFileName);
    
    if (FileOrErr.getError()) {
        return nullptr;
    }

    srcMgr.AddNewSourceBuffer(std::move(*FileOrErr), SMLoc());
    TGParser Parser(srcMgr, ArrayRef<std::string>(), *records);
    
    if (Parser.ParseFile()) return nullptr;
    
    return records;
}

PYBIND11_MAKE_OPAQUE(std::vector<std::string>);

void init_RecordKeeper(py::module &);
void init_Record(py::module &);

void init_Type(py::module& m) {
    py::bind_vector<std::vector<std::string>>(m, "StringVector");
    py::implicitly_convertible<py::iterable, std::vector<std::string>>();
}

PYBIND11_MODULE(tablegen, m) {
    m.doc() = "pybind11 example plugin";
    m.def("add", &add, "A function which adds two numbers");
    init_Type(m);
    init_Record(m);
    init_RecordKeeper(m);

    m.def("ParseTableGen", &ParseTableGen);
}