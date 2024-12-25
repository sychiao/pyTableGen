
cmake_minimum_required(VERSION 3.22)
project(tablegen-py)

#if(NOT DEFINED pybind11_SOURCE_DIR)
#  message(STATUS "Not find pybind11 try to download one")
#  include(cmake/pybind11.cmake)
#endif()

# add_subdirectory(pybind11)

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

configure_file(
    ${CMAKE_CURRENT_SOURCE_DIR}/LLVMSource.cpp.in
    ${CMAKE_CURRENT_SOURCE_DIR}/LLVMSource.cpp
    @ONLY
)

#set (CMAKE_CXX_STANDARD 14)

pybind11_add_module(tablegen
    SHARED
    main_module.cpp
    LLVMSource.cpp
    lib/RecordKeeper.cpp
    lib/Init.cpp
    lib/Record.cpp
    lib/BindType.cpp
    lib/RecTy.cpp
)

message(STATUS "install tablegen binding to ${CMAKE_BINARY_DIR}/pyTableGen/src/tablegen")

set_target_properties(tablegen
    PROPERTIES
    OUTPUT_NAME binding
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/../pyTableGen/src/tablegen"
)

# pybind11-stubgen -o . tablegen.binding
if(${Found_pybind11_stubgen} EQUAL 0)
    add_custom_command(TARGET tablegen POST_BUILD
        COMMAND ${Python3_EXECUTABLE} -m pybind11_stubgen -o . tablegen.binding
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/../pyTableGen/src
        COMMENT "Generating .pyi files using pybind11-stubgen"
    )
else()
    message(WARNING "pybind11_stubgen not found, skip generating .pyi files")
endif()

target_include_directories(tablegen PUBLIC
    ${LLVM_MAIN_SRC_DIR}/lib/TableGen
    include/
)

target_link_libraries(tablegen PRIVATE LLVMTableGen LLVMSupport)
