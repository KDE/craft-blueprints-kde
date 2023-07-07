# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ template library for linear algebra"
        self.webpage = "http://eigen.tuxfamily.org/"

        # just support one version
        for ver in ["3.3.9", "3.4.0"]:
            self.targets[ver] = f"https://gitlab.com/libeigen/eigen/-/archive/{ver}/eigen-{ver}.tar.bz2"
            self.archiveNames[ver] = f"eigen-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"eigen-{ver}"

        # 3.3.9
        self.targetDigests["3.3.9"] = (["0fa5cafe78f66d2b501b43016858070d52ba47bd9b1016b0165a7b8e04675677"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.3.9"] = [("0001-Remove-bogus-CMake-build-type-check.patch", 1), ("eigen3-pc-cmake-installdirs.patch", 0)]
        self.patchLevel[ver] = 2

        # 3.4.0
        self.targetDigests["3.4.0"] = (["b4c198460eba6f28d34894e3a5710998818515104d6e74e5cc331ce31e46e626"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.4.0"] = [("eigen3-pc-cmake-installdirs-3.4.0.diff", 1)]

        self.defaultTarget = "3.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DEIGEN_TEST_NOQT=ON -DBUILD_TESTING=ON"
