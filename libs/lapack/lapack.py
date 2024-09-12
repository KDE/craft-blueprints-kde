# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Linear Algebra PACKage."
        self.webpage = "https://www.netlib.org/lapack"
        self.displayName = "lapack"
        self.patchToApply["3.9.0"] = [
            ("0001-Restore-Missing-Prototypes.patch", 1),  # https://github.com/Reference-LAPACK/lapack/commit/87536aa3.patch
            ("0002-Fix-mingw-build.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args += ["-DCMAKE_SKIP_RPATH=ON", "-DLAPACKE_WITH_TMG=ON", "-DCBLAS=ON", "-DBUILD_DEPRECATED=ON"]
        # mingw-w64 (gfortran) 8.1 includes only static libgfortran and fails to build dll
        self.subinfo.options.dynamic.buildStatic = True if CraftCore.compiler.platform.isWindows else False
