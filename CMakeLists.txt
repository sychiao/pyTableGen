project(tablegen-py)

cmake_minimum_required(VERSION 3.22)
include(cmake/pybind11.cmake)
# include(cmake/llvm.cmake)

set(LLVM_DIR build/llvm/lib/cmake/llvm)
find_package(LLVM REQUIRED CONFIG)

message(STATUS "Using LLVM ${LLVM_PACKAGE_VERSION}")

add_definitions(${LLVM_DEFINITIONS})
include_directories(${LLVM_INCLUDE_DIRS})
link_directories(${LLVM_LIBRARY_DIR})

list(APPEND CMAKE_MODULE_PATH "${LLVM_CMAKE_DIR}")
include(AddLLVM)

set(LLVM_LINK_COMPONENTS TableGen Support)

pybind11_add_module(foo 
    SHARED foo.cpp)

target_include_directories(foo PUBLIC
    build/src/llvm/llvm/lib/TableGen
)

llvm_map_components_to_libnames(
    llvm_libs ${LLVM_LINK_COMPONENTS})
target_link_libraries(foo PRIVATE ${llvm_libs})
