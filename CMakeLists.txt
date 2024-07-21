function(checkPythonPackage package)
  execute_process(COMMAND ${Python3_EXECUTABLE} -c "import ${package}"
    OUTPUT_VARIABLE ${package}_output
    ERROR_VARIABLE  ${package}_error
    RESULT_VARIABLE ${package}_result)
  if(NOT ${${package}_result} EQUAL 0)
    message(WARNING "${package} package not available: ${${package}_error}")
  endif()
endfunction()

find_package(Python COMPONENTS Interpreter Development)
message(STATUS "Checking Python packages with ${Python3_EXECUTABLE}")
checkPythonPackage(pytest)
checkPythonPackage(pyyaml)

add_subdirectory(tablegen-binding)
add_subdirectory(pyTableGen)
