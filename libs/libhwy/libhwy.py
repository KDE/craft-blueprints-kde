# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2.0", "1.4.0"]:
            self.targets[ver] = f"https://github.com/google/highway/releases/download/{ver}/highway-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"highway-{ver}"
        self.targetDigests["1.2.0"] = (["58e9d5d41d6573ad15245ad76aec53a69499ca7480c092d899c4424812ed906f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4.0"] = (["36f672ab48ddb3c8555e9e89e16fe400cd7d16c6eb455a1a3d0c146a63ababdc"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Performance-portable, length-agnostic SIMD with runtime dispatch"
        self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DHWY_ENABLE_CONTRIB=OFF", "-DHWY_ENABLE_EXAMPLES=OFF", "-DHWY_ENABLE_TESTS=OFF"]
