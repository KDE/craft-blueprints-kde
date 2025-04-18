# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A collection of multi-dimensional data structure and indexing algorithm"

        for ver in ["2.1.1", "3.0.0"]:
            self.targets[ver] = f"https://gitlab.com/api/v4/projects/mdds%2Fmdds/packages/generic/source/{ver}/mdds-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"mdds-{ver}"
        self.targetDigests["2.1.1"] = (["1483d90cefb8aa4563c4d0a85cb7b243aa95217d235d422e9ca6722fd5b97e56"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.0"] = (["9b077e8d929050e9a432cc131beed2380ac85cfe98b17fc26d01d0ed532129c8"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.1.1"] = [("mdds-2.1.1_MSVC-c++17.patch", 1)]
            # the new ax_cxx_compile_stdcxx.m4 does not work, using the old one from 2.1.1
            self.patchToApply["3.0.0"] = [("mdds-3.0.0_MSVC-c++17.patch", 1)]

        self.defaultTarget = "3.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.isMSVC():
            # MSVC explicitly needs to update __cplusplus
            # https://devblogs.microsoft.com/cppblog/msvc-now-correctly-reports-__cplusplus/
            self.subinfo.options.configure.cxxflags += "/Zc:__cplusplus"
