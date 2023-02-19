#include <pybind11/pybind11.h>

namespace py = pybind11;
void init_RecordKeeper(py::module &);
void init_Record(py::module &);
void init_RecordVal(py::module &);
void init_Type(py::module& m);