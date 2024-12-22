llvm-cov report \
  src/tablegen/binding.cpython-*.so \
  -instr-profile=cov_data/cov.profdata \
  -ignore-filename-regex='(.*/lib/Demangle/ItaniumDemangle.cpp)|
                          |(.*/lib/TableGen/Error.cpp)|
                          |(.*/lib/TableGen/TG.*)|
                          |(.*/include/llvm/Demangle/.*)|
                          |(.*/include/llvm/Support/.*)|
                          |(.*/include/llvm/ADT/.*)|
                          |(.*/lib/Support/.*)|
                          |(.*/include/llvm/Config/.*)'
