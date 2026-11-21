# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/fmtlib/fmt.git"

        for ver in ["12.2.0"]:
            self.targets[ver] = f"https://github.com/fmtlib/fmt/releases/download/{ver}/fmt-{ver}.zip"
            self.targetInstSrc[ver] = f"fmt-{ver}"
        self.targetDigests["12.2.0"] = (["a2f4a8d51178f954e4c339007f77edd76ba0cb2e36f87a48e5a5403d9be5878f"], CraftHash.HashAlgorithm.SHA256)

        self.releaseManagerId = 11526

        self.description = "A modern formatting library"
        self.webpage = "https://fmt.dev"
        self.defaultTarget = "12.2.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DFMT_DOC=OFF",
            f"-DFMT_TEST={self.subinfo.options.dynamic.buildTests.asOnOff}",
        ]
