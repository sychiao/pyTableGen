#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "TGParser.h"
#include "BindInit.h"

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


PYBIND11_MODULE(tablegen, m) {
    m.doc() = "pybind11 example plugin";

    init_Type(m);
    init_Record(m);
    init_RecordKeeper(m);
    init_RecordVal(m);

    m.def("ParseTableGen", &ParseTableGen);
}