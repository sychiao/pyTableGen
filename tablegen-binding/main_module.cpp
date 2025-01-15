#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <llvm/TableGen/Parser.h>
#include "TGParser.h"
#include "BindType.h"
#include "BindImpl.h"
#include "BindRecTy.h"
#include "BindInit.h"
#include "BindRecord.h"

using namespace llvm;

std::string getLLVMSourceRoot();

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
    if (TableGenParseFile(srcMgr, *records, Macros))
        return nullptr;
    /*
    TGParser Parser(srcMgr, Macros, *records);
    if (Parser.ParseFile()) return nullptr;
    */

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

    /* for pybind11-stubgen we need define class first then define method*/
    _RecordBindingImpl RecordBindingImpl(m);
    _RecTyBindingImpl RecTyBinding(m);
    _InitBindingImpl InitBinding(m);

    /*define method*/
    def_Type(m);
    RecordBindingImpl.def();
    RecTyBinding.def();
    InitBinding.def();

    m.def("getLLVMSourceLoc", &getLLVMSourceRoot);
    m.def("ParseTableGen",
        py::overload_cast<std::string>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>, std::vector<std::string>>(&ParseTableGen));
}