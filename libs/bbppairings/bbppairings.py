# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Manuel Alcaraz Zambrano <manuel@alcarazzam.dev>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "bbpPairings"
        self.description = "Swiss-system chess tournament pairing engine"

        self.svnTargets["master"] = (
            "https://github.com/BieremaBoyzProgramming/bbpPairings.git"
        )

        for ver in ["6.0.0"]:
            self.targets[ver] = (
                f"https://github.com/BieremaBoyzProgramming/bbpPairings/archive/refs/tags/v{ver}.tar.gz"
            )
            self.archiveNames[ver] = f"bbppairings-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"bbpPairings-{ver}"

        self.targetDigests["6.0.0"] = (
            ["b7f95c0803131e38a56e8829bd062d9ad51908322dd6fef01380b2f612f58227"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.defaultTarget = "6.0.0"

        for ver in ["master", "6.0.0"]:
            self.patchToApply[ver] = [("0001-Add-CMake-build.patch", 1)]
            self.patchLevel[ver] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_CXX_FLAGS=-DOMIT_GENERATOR"]
