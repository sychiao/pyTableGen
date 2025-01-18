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

void def_Type(py::module& m);

class BindInit : public Init { // helper type for exposing protected functions
public:
    using Init::InitKind; // inherited with different access modifier
};

class BindBinOpInit : public BinOpInit {
public:
    using BinOpInit::BinaryOp;
};


using pyInitKindEnum = py::enum_<BindInit::InitKind>;
using pyBinaryOpEnum = py::enum_<BindBinOpInit::BinaryOp>;
using pyStringFormatEnum = py::enum_<StringInit::StringFormat>;

using pyInitClass = py::class_<Init>;
using pyTypedInitClass = py::class_<TypedInit, Init>;
using pyUnsetInitClass = py::class_<UnsetInit, TypedInit>;

using pyBitInitClass     = py::class_<BitInit, TypedInit>;
using pyBitsInitClass    = py::class_<BitsInit, TypedInit>;
using pyIntInitClass     = py::class_<IntInit, TypedInit>;
using pyDagInitClass     = py::class_<DagInit, TypedInit>;
using pyListInitClass    = py::class_<ListInit, TypedInit>;
using pyStringInitClass = pybind11::class_<llvm::StringInit, llvm::TypedInit>;

using pyDefInitClass     = py::class_<DefInit, TypedInit>;
using pyVarInitClass     = py::class_<VarInit, TypedInit>;
using pyVarBitInitClass  = py::class_<VarBitInit, TypedInit>;

using pyCondOpInitClass  = py::class_<CondOpInit, TypedInit>;
using pyOpInitClass = py::class_<OpInit, TypedInit>;
using pyBinOpInitClass = py::class_<BinOpInit, OpInit>;




struct _InitBindingImpl {
  pyInitKindEnum     pyinitkind;
  pyBinaryOpEnum     pybinop;
  pyStringFormatEnum pystrenum;

  pyInitClass        pyinitcls;
  pyTypedInitClass   pytypedinitcls;
  pyUnsetInitClass   pyunsetinitcls;

  /* Subclass of TypedInit*/
  pyBitInitClass       pybitinitcls;
  pyBitsInitClass      pybitsinitcls;
  pyIntInitClass       pyintinitcls;
  pyStringInitClass    pystringinitcls;
  pyListInitClass      pylistinitcls;
  pyDagInitClass       pydaginitcls;

  /* Subclass of Ops*/
  // pyCondOpInitClass    pycondopinitcls;
  //pyExistsOpInitClass  pyexistsopinitcls;
  pyOpInitClass        pyopinitcls;
  pyBinOpInitClass     pybinopinitcls;

  /* Var/Def */
  pyDefInitClass       pydefinitcls;
  pyVarInitClass       pyvarinitcls;
  pyVarBitInitClass    pyvarbitinitcls;

 

  _InitBindingImpl(py::module &m) : 
    pyinitkind(m, "InitKind"),
    pybinop(m, "BinaryOp"),
    pystrenum(m, "StringFormat"),
    pyinitcls(m, "Init"),
    pytypedinitcls(m, "TypedInit"),
    pyunsetinitcls(m, "UnsetInit"),
    pybitinitcls(m, "BitInit"),
    pybitsinitcls(m, "BitsInit"),
    pyintinitcls(m, "IntInit"),
    pystringinitcls(m, "StringInit"),
    pylistinitcls(m, "ListInit"),
    pydaginitcls(m, "DagInit"),
    pyopinitcls(m, "OpInit"),
    pybinopinitcls(m, "BinOpInit"),
    pydefinitcls(m, "DefInit"),
    pyvarinitcls(m, "VarInit"),
    pyvarbitinitcls(m, "VarBitInit")
    {}

    void _def(pyInitKindEnum &);
    void _def(pyBinaryOpEnum &);
    void _def(pyStringFormatEnum &);

    void _def(pyInitClass &) ;
    void _def(pyTypedInitClass &);
    void _def(pyUnsetInitClass &);

    // Values
    void _def(pyBitInitClass &);
    void _def(pyBitsInitClass &);
    void _def(pyIntInitClass &);
    void _def(pyListInitClass &);
    void _def(pyStringInitClass &);
    void _def(pyDagInitClass &);


    // Ops
    void _def(pyOpInitClass &) ;
    void _def(pyBinOpInitClass &);

    // Var
    void _def(pyDefInitClass &);
    void _def(pyVarInitClass &);
    void _def(pyVarBitInitClass &cls);


    // void _def()
    

    void def() {
        _def(pyinitkind);
        _def(pybinop);
        _def(pystrenum);
        _def(pyinitcls);
        _def(pytypedinitcls);
        _def(pyunsetinitcls);
        _def(pybitinitcls);
        _def(pybitsinitcls);
        _def(pyintinitcls);
        _def(pystringinitcls); 
        _def(pydaginitcls);
        _def(pylistinitcls);
        _def(pyopinitcls);
        _def(pybinopinitcls);
        _def(pydefinitcls);
        _def(pyvarinitcls);
        _def(pyvarbitinitcls);
    }
};

void def_InitKind(py::module &m);
void def_other_Init(py::module &m);
