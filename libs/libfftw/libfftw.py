# -*- coding: utf-8 -*-
import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["3.3.8"] = "http://www.fftw.org/fftw-3.3.8.tar.gz"
        self.patchToApply["3.3.8"] = [("libfftw-3.3.8-20200429.diff", 1)]
        if CraftCore.compiler.isWindows:
            self.patchToApply["3.3.8"].append(("libfftw-win32-aligned-malloc.patch", 0))
        self.targetDigests["3.3.8"] = "59831bd4b2705381ee395e54aa6e0069b10c3626"
        self.targetInstSrc["3.3.8"] = "fftw-3.3.8"
        self.patchLevel["3.3.8"] = 1
        self.description = "a C subroutine library for computing the discrete Fourier transform (DFT)"

        self.defaultTarget = "3.3.8"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DENABLE_AVX=OFF",
            "-DENABLE_THREADS=ON",
            "-DWITH_COMBINED_THREADS=ON",
        ]
        if CraftCore.compiler.architecture & CraftCompiler.Architecture.x86:
            self.subinfo.options.configure.args += ["-DENABLE_SSE2=ON"]
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += [
                "-DWITH_OUR_MALLOC=ON",
                "-DFFTW_ENABLE_ALLOCA=OFF",
                "-DWINDOWS_F77_MANGLING=ON",
            ]
