# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildType", "Release")

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/doxygen/doxygen.git"

        for ver in ["1.18.0"]:
            self.targets[ver] = f"https://www.doxygen.nl/files/doxygen-{ver}.src.tar.gz"
            self.targetInstSrc[ver] = f"doxygen-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["1.18.0"] = (["a1deed70a6785bbec95a2b2a9e419dc7f7b223a9d74a8644ae611c8e2dcdd354"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.18.0"] = [("doxygen-1.18.0-20261016.diff", 1)]

        self.releaseManagerId = 457

        self.description = "Doxygen is the de facto standard tool for generating documentation from annotated C++ sources"
        self.webpage = "https://www.doxygen.nl"
        self.defaultTarget = "1.18.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["libs/python"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/spdlog"] = None
        self.runtimeDependencies["libs/fmt"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # race condition with flex
        if CraftCore.compiler.platform.isWindows:
            self.subinfo.options.make.supportsMultijob = False
        self.subinfo.options.configure.args += [
            "-Duse_sys_sqlite3=ON",
            "-Duse_sys_spdlog=ON",
            "-Duse_sys_fmt=ON",
            "-Dbuild_wizard=OFF",
            "-Dbuild_doc=OFF",
            "-Dbuild_search=OFF",
            "-Duse_libclang=OFF",
        ]
