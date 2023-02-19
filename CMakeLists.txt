
cmake_minimum_required(VERSION 3.22)
project(tablegen-py)

if(NOT DEFINED pybind11_SOURCE_DIR)
  message(STATUS "Not find pybind11 try to download one")
  include(cmake/pybind11.cmake)
endif()
add_subdirectory(${pybind11_SOURCE_DIR})

set(LLVM_PREFIX /home/ycsu/Develop/TableGen.py-dev/llvm-project/install)
set(LLVM_DIR ${LLVM_PREFIX}/lib/cmake/llvm)
find_package(LLVM REQUIRED CONFIG)

message(STATUS "Using LLVM ${LLVM_PACKAGE_VERSION}")

add_definitions(${LLVM_DEFINITIONS})
include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIR})

list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)
set (CMAKE_CXX_STANDARD 14)

set(LLVM_LINK_COMPONENTS TableGen Support)
# set(CMAKE_CXX_FLAGS "-g -O0 -fprofile-arcs -ftest-coverage")
# set(CMAKE_C_FLAGS   "-g -O0 -fprofile-arcs -ftest-coverage")

pybind11_add_module(tablegen 
    SHARED
    main_module.cpp
    lib/Record.cpp
    lib/BindType.cpp
)

target_include_directories(tablegen PUBLIC
    /home/ycsu/Develop/TableGen.py-dev/llvm-project/llvm/lib/TableGen
    include/
)

llvm_map_components_to_libnames(
    llvm_libs ${LLVM_LINK_COMPONENTS})
target_link_libraries(tablegen PRIVATE ${llvm_libs})
