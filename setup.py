import os
import re
import subprocess
import sys
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext

# A CMakeExtension needs a sourcedir instead of a file list.
# The name must be the _single_ output extension from the CMake build.
# If you need multiple extensions, see scikit-build.
class CMakeExtension(Extension):
    def __init__(self, name: str, sourcedir: str = "") -> None:
        super().__init__(name, sources=[])
        self.sourcedir = os.fspath(Path(sourcedir).resolve())


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        ext_fullpath = Path.cwd() / self.get_ext_fullpath(ext.name)  # type: ignore[no-untyped-call]
        ext_module_dir = ext_fullpath.parent.resolve()

        subprocess.run(["cmake", "--preset=default"
                               , f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={ext_module_dir}{os.sep}"
                               , f"-DPYTHON_EXECUTABLE={sys.executable}"], check=True)
        subprocess.run(["cmake", "--build", "--preset=default"], check=True)


# The information here can also be placed in setup.cfg - better separation of
# logic and declaration, and simpler if you include description/version in a file.
setup(
    name="tablegen",
    version="0.0.1",
    author="Su, Yi-Chiao",
    description="A project using pybind11 and CMake",
    long_description="",
    ext_modules=[CMakeExtension("tablegen")],
    cmdclass={"build_ext": CMakeBuild},
    zip_safe=False,
    extras_require={"test": ["pytest>=6.0"]},
    python_requires=">=3.7",
)
