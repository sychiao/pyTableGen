#include <pybind11/pybind11.h>
#include <pybind11/stl_bind.h>
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/FileSystem.h"
#include "llvm/Support/MemoryBuffer.h"
#include "llvm/Support/ToolOutputFile.h"
#include "llvm/TableGen/Error.h"
#include "llvm/TableGen/Main.h"
#include "llvm/TableGen/Record.h"

#include "BindType.h"
#include "BindRecord.h"

#include <iostream>

namespace py = pybind11;
using namespace llvm;

struct RecordKeeper_Impl {
  static std::map<std::string, Record*, std::less<>> getClasses(llvm::RecordKeeper &Self) {
    std::map<std::string, Record*, std::less<>> ret;
    for (const auto& kv : Self.getClasses()) {
          ret[kv.first] = kv.second.get();
    }
    return ret;
  }

  static std::map<std::string, Record*, std::less<>> getDefs(llvm::RecordKeeper &Self) {
    std::map<std::string, Record*, std::less<>> ret;
    for (const auto& kv : Self.getDefs()) {
          ret[kv.first] = kv.second.get();
    }
    return ret;
  }

  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, py::args args) {
        auto clsnames = args.cast<std::vector<std::string>>();
        return RecordKeeper_Impl::getAllDerivedDefinitions(Self, clsnames);
  }

  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, std::string clsname) {
        return Self.getAllDerivedDefinitions(clsname);
  }

  static std::vector<Record*> getAllDerivedDefinitions(RecordKeeper &Self, std::vector<std::string> &clsnames) {
        auto castVec = std::vector<StringRef>(clsnames.begin(), clsnames.end());
        return Self.getAllDerivedDefinitions(	ArrayRef<StringRef>(castVec.data(), castVec.size()));
  }
};

void _RecordBindingImpl::_def(pyRecordKeeperClass &cls) {
    cls.def(py::init<>())
      .def("getInputFilename", [](llvm::RecordKeeper &Self) {
            return Self.getInputFilename();
        }, py::return_value_policy::reference)
      .def("getClasses", &RecordKeeper_Impl::getClasses, py::return_value_policy::reference)
      .def("getClass", [](llvm::RecordKeeper &Self, std::string clsname) {
            return Self.getClass(clsname);
        }, py::return_value_policy::reference)
      .def("getDefs", *RecordKeeper_Impl::getDefs, py::return_value_policy::reference)
      .def("getDef", [](llvm::RecordKeeper &Self, std::string clsname){
            return Self.getDef(clsname);
        }, py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, std::string> (&RecordKeeper_Impl::getAllDerivedDefinitions),
        py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, std::vector<std::string>&> (&RecordKeeper_Impl::getAllDerivedDefinitions),
        py::return_value_policy::reference)
      .def("getAllDerivedDefinitions",
        py::overload_cast<llvm::RecordKeeper&, py::args> (&RecordKeeper_Impl::getAllDerivedDefinitions), 
        py::return_value_policy::reference)
    ;
}