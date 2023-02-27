#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>

#include "TGParser.h"
#include "BindImpl.h"

using namespace llvm;

RecordKeeper* _ParseTableGen(std::string InputFileName,
    std::vector<std::string> IncludeDirs,
    std::vector<std::string> Macros
) {
    RecordKeeper* records = new RecordKeeper();
    auto srcMgr = SourceMgr();
    ErrorOr<std::unique_ptr<MemoryBuffer>> FileOrErr 
        = MemoryBuffer::getFile(InputFileName);
    
    if (FileOrErr.getError()) { return nullptr; }

    srcMgr.AddNewSourceBuffer(std::move(*FileOrErr), SMLoc());
    srcMgr.setIncludeDirs(IncludeDirs);
    TGParser Parser(srcMgr, Macros, *records);
    
    if (Parser.ParseFile()) return nullptr;
    
    return records;
}

RecordKeeper* ParseTableGen(std::string InputFileName) {
    return _ParseTableGen(InputFileName, std::vector<std::string>(), std::vector<std::string>());
}

RecordKeeper* ParseTableGen(std::string InputFileName, std::vector<std::string> IncludeDirs) {
    return _ParseTableGen(InputFileName, IncludeDirs, std::vector<std::string>());
}

RecordKeeper* ParseTableGen(std::string InputFileName, std::vector<std::string> IncludeDirs, std::vector<std::string> macros) {
    return _ParseTableGen(InputFileName, IncludeDirs, macros);
}

PYBIND11_MODULE(binding, m) {
    m.attr("__name__") = "tablegen.binding";
    m.doc() = "pybind11 example plugin";

    def_Type(m);
    def_Record(m);
    def_RecordKeeper(m);
    def_RecordVal(m);
    def_Init(m);

    m.def("ParseTableGen",
        py::overload_cast<std::string>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>, std::vector<std::string>>(&ParseTableGen));
}