include(ExternalProject)

ExternalProject_Add(
    llvm
    PREFIX ${CMAKE_CURRENT_BINARY_DIR}
    SOURCE_SUBDIR llvm
    GIT_REPOSITORY /home/ycsu/Develop/RISCV-dev/llvm-project
    GIT_TAG release/15.x
    GIT_SHALLOW ON
    GIT_PROGRESS ON
    CMAKE_GENERATOR Ninja
    CMAKE_ARGS
        -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_BINARY_DIR}/llvm
        -DCMAKE_BUILD_TYPE=Release
        -DLLVM_ENABLE_ASSERTIONS=ON
        -DLLVM_ENABLE_RTTI=ON
        -DLLVM_ENABLE_EH=ON
    CMAKE_CACHE_ARGS
        -DLLVM_DISTRIBUTION_COMPONENTS:STRING=llvm-headers;cmake-exports;LLVMDemangle;LLVMSupport;LLVMTableGen;llvm-config
    BUILD_COMMAND ninja distribution
    INSTALL_COMMAND ninja install-distribution
)
