# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/gabime/spdlog.git"

        for ver in ["1.17.0"]:
            self.targets[ver] = f"https://github.com/gabime/spdlog/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"spdlog-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"spdlog-{ver}"
        self.targetDigests["1.17.0"] = (["d8862955c6d74e5846b3f580b1605d2428b11d97a410d86e2fb13e857cd3a744"], CraftHash.HashAlgorithm.SHA256)
        self.releaseManagerId = 15599

        self.description = "Fast C++ logging library"
        self.webpage = "https://github.com/gabime/spdlog"
        self.defaultTarget = "1.17.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/fmt"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DSPDLOG_FMT_EXTERNAL=ON",
            f"-DSPDLOG_BUILD_SHARED={self.subinfo.options.dynamic.buildStatic.inverted.asOnOff}",
            "-DSPDLOG_BUILD_EXAMPLE=OFF",
            f"-DSPDLOG_BUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
        ]
