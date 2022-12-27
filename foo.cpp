#include<pybind11/pybind11.h>

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


PYBIND11_MODULE(foo, m) {
    m.doc() = "pybind11 example plugin";
    m.def("add", &add, "A function which adds two numbers");

    py::class_<Record>(m, "Record")
      .def("getName", [](Record &Self) {return Self.getName().str();});

    py::class_<llvm::RecordKeeper>(m, "RecordKeeper")
      .def(py::init<>())
      .def("getClass", [](llvm::RecordKeeper &Self, std::string clsname) {
            return Self.getClass(clsname);
        },
        py::return_value_policy::reference
    );

    m.def("ParseTableGen", &ParseTableGen);
}