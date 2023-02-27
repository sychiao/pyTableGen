#include <pybind11/pybind11.h>

namespace py = pybind11;
void def_RecordKeeper(py::module &);
void def_Record(py::module &);
void def_RecordVal(py::module &);
void def_Type(py::module& m);
void def_Init(py::module& m);