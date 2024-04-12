# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.7"]:
            self.targets[ver] = f"https://github.com/google/highway/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"highway-{ver}"
        self.targetDigests["1.0.7"] = (["5434488108186c170a5e2fca5e3c9b6ef59a1caa4d520b008a9b8be6b8abe6c5"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Performance-portable, length-agnostic SIMD with runtime dispatch"
        self.defaultTarget = "1.0.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DHWY_ENABLE_EXAMPLES=OFF", "-DHWY_ENABLE_TESTS=OFF"]
