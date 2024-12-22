mkdir -p cov_data
LLVM_PROFILE_FILE="cov_data/cov.profraw" python3 -m pytest --cov-report=lcov:cov_data/cov.info --cov=src 
llvm-profdata merge -sparse cov_data/cov.profraw -o cov_data/cov.profdata
