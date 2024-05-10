# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Volker Krause <vkrause@kde.org>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Recast Navigation"

        for ver in ["1.6.0"]:
            self.targets[ver] = f"https://github.com/recastnavigation/recastnavigation/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"recastnavigation-{ver}"
        self.targetDigests["1.6.0"] = (["d48ca0121962fa0639502c0f56c4e3ae72f98e55d88727225444f500775c0074"], CraftHash.HashAlgorithm.SHA256)
        self.targets["main"] = "https://github.com/recastnavigation/recastnavigation.git"

        self.defaultTarget = "1.6.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            "-DRECASTNAVIGATION_DEMO=OFF",
            "-DRECASTNAVIGATION_EXAMPLES=OFF",
            "-DRECASTNAVIGATION_TESTS=OFF",
        ]

        if self.subinfo.options.buildStatic:
            self.subinfo.options.configure.args += ["-DCMAKE_POSITION_INDEPENDENT_CODE=ON"]
