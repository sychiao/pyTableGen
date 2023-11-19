#git clone git@github.com:llvm/llvm-project.git --depth=1 -b release/15.x 
#ln -s <llvm_path> llvm-project
ln -s `pwd` llvm-project/llvm/utils/pyTableGen
echo 'add_subdirectory(utils/pyTableGen)' >> llvm-project/llvm/CMakeLists.txt
mkdir build
cmake -S llvm-project/llvm \
      -B build \
	-DCMAKE_BUILD_TYPE=RelWithDebInfo\
	-DCMAKE_C_COMPILER=clang\
	-DCMAKE_CXX_COMPILER=clang++\
	-DLLVM_BUILD_INSTRUMENTED_COVERAGE=ON \
	-DLLVM_ENABLE_RTTI=ON \
	-DLLVM_CODE_COVERAGE_TARGETS=LLVMTableGen
cmake --build build -t tablegen -j4
