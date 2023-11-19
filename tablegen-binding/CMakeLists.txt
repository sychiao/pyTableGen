
cmake_minimum_required(VERSION 3.22)
project(tablegen-py)

#if(NOT DEFINED pybind11_SOURCE_DIR)
#  message(STATUS "Not find pybind11 try to download one")
#  include(cmake/pybind11.cmake)
#endif()
find_package(Python COMPONENTS Interpreter Development)
add_subdirectory(pybind11)

if(NOT DEFINED LLVM_MAIN_SRC_DIR)
	#set(LLVM_PREFIX <set path of llvm install prefix>)
    set(LLVM_DIR ${LLVM_PREFIX}/lib/cmake/llvm)
    find_package(LLVM REQUIRED CONFIG)
    message(STATUS "Using LLVM ${LLVM_PACKAGE_VERSION}")
    add_definitions(${LLVM_DEFINITIONS})
    include_directories(${LLVM_INCLUDE_DIRS})
    link_directories(${LLVM_LIBRARY_DIR})
    list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
    include(AddLLVM)
endif()

#set (CMAKE_CXX_STANDARD 14)

pybind11_add_module(tablegen 
    SHARED
    main_module.cpp
    lib/RecordKeeper.cpp
    lib/Init.cpp
    lib/Record.cpp
    lib/BindType.cpp
    lib/RecTy.cpp
)

message(STATUS "install tablegen binding to ${CMAKE_CURRENT_SOURCE_DIR}/../src/tablegen")

set_target_properties(tablegen
    PROPERTIES
    OUTPUT_NAME binding
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../src/tablegen"
)

target_include_directories(tablegen PUBLIC
    ${LLVM_MAIN_SRC_DIR}/lib/TableGen
    include/
)

target_link_libraries(tablegen PRIVATE LLVMTableGen LLVMSupport)
