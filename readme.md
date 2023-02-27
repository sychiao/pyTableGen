# py-TableGen

TableGen of LLVM is a awesome tool to describe "Data".
However, write TableGen in C++ with LLVM project is a little "heavy".
py-TableGen provide an binding for tablegen, so we can develop tablegen backend with python.
And we can use python to analysis exists td file(table describption), and edit them.
An python based embedded TableGEn-like language also provide.

# Progress Record
## TableGen Binding
  - [ ] TableGen Binding Support, LLVMTableGen Coverage should over 50%
    - Workflow
      - [ ] Support pytest/coverage/lcov framework
      - [ ] Standard build/install flow
    - Feature
      - [ ] Support RecordKeeper
      ...
  - [ ] Support Parsing real td file in LLVM Project
## TableGen Core
  - [ ] Translate object from td to native Python objects
  ...

## TableGen DSL
    ...