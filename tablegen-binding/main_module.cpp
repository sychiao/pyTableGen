#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include <llvm/TableGen/Parser.h>
#include "TGParser.h"
#include "BindType.h"
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
    if (TableGenParseFile(srcMgr, *records))
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

    auto recordkeepercls = pyRecordKeeperClass(m, "RecordKeeper");
    auto smloccls = pySMLocClass(m, "SMLoc");
    auto recordcls = pyRecordClass(m, "Record");
    auto recordvalcls = pyRecordValClass(m, "RecordVal");
    auto recTyKindEnum = pyRecTyKindEnum(m, "RecTyKind");
    auto recTycls = pyRecTyClass(m, "RecTy");

    auto initcls = pyInitClass(m, "Init");
    auto typedinitcls = pyTypedInitClass(m, "TypedInit");
    auto opinitcls = pyOpInitClass(m, "OpInit");
    auto binopcls = pyBinOpInitClass(m, "BinOpInit");
    auto recordrecTycls = pyRecordRecTyClass(m, "RecordRecTy");
    auto stringinitcls = pyStringInitClass(m, "StringInit");

    /* for pybind11-stubgen we need define class first then define method*/
    def_Type(m);
    def_SMLoc(smloccls);
    def_Init(initcls);
    def_StringInit(stringinitcls);
    def_InitKind(m);
    def_other_Init(m);
    def_Record(recordcls);
    def_RecordRecTy(m, recordrecTycls);
    def_RecordKeeper(recordkeepercls);
    def_RecordVal(recordvalcls);
    def_RecTy(recTycls);
    def_RecTyKind(recTyKindEnum);

    m.def("ParseTableGen",
        py::overload_cast<std::string>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>>(&ParseTableGen));
    m.def("ParseTableGen",
        py::overload_cast<std::string, std::vector<std::string>, std::vector<std::string>>(&ParseTableGen));
}