mkdir -p cov_data
LLVM_PROFILE_FILE="cov_data/cov.profraw" python3 -m pytest --cov-report=lcov:cov_data/cov.info --cov=src 
llvm-profdata merge -sparse cov_data/cov.profraw -o cov_data/cov.profdata
llvm-cov export -instr-profile cov_data/cov.profdata src/tablegen/binding.cpython-310-x86_64-linux-gnu.so -format=lcov > cov_data/bind.lcov
lcov -a cov_data/bind.lcov -a cov_data/cov.info -o cov_data/merge.info
lcov -e cov_data/merge.info -o cov_data/final.info \
    '*lib/TableGen/*' \
    '*include/llvm/TableGen/*' \
    '*/TableGen.py/src/tablegen/*' \
    '*/pyTableGen/tablegen-binding/*'
genhtml cov_data/final.info -o cov_report
