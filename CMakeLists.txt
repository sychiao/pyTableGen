macro(checkPythonPackage package)
  execute_process(COMMAND ${Python3_EXECUTABLE} -c "import ${package}"
    OUTPUT_VARIABLE ${package}_output
    ERROR_VARIABLE  ${package}_error
    RESULT_VARIABLE Found_${package})
  if(NOT ${Found_${package}} EQUAL 0)
    message(WARNING "${package} package not available: ${${package}_error}")
  endif()
endmacro()

find_package(Python3 3.12 COMPONENTS Interpreter Development)
message(STATUS "Checking Python packages with ${Python3_EXECUTABLE}")
checkPythonPackage(pytest)
checkPythonPackage(yaml)
checkPythonPackage(pybind11)
checkPythonPackage(pybind11_stubgen)

message(STATUS "Found stubgen: ${Found_pybind11_stubgen}")

# found pybind11 with python
execute_process(COMMAND ${Python3_EXECUTABLE} -m pybind11 --cmakedir
  OUTPUT_VARIABLE pybind11_output
  RESULT_VARIABLE pybind11_result
  OUTPUT_STRIP_TRAILING_WHITESPACE)

if(NOT ${pybind11_result} EQUAL 0)
  message(STATUS "pybind11 not found with python environment")
else()
  message(STATUS "Found pybind11: ${pybind11_output}")
  set(pybind11_ROOT ${pybind11_output})
endif()

find_package(pybind11)
if(NOT pybind11_FOUND)
  message(WARNING "pybind11 not found, disable pyTableGen")
else()
  message(STATUS "Found pybind11: ${pybind11_INCLUDE_DIRS}")
  add_subdirectory(tablegen-binding)
  add_subdirectory(pyTableGen)
endif()
