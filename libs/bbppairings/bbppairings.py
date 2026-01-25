# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Manuel Alcaraz Zambrano <manuel@alcarazzam.dev>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "bbpPairings"
        self.description = "Swiss-system chess tournament engine"

        self.svnTargets["v6"] = (
            "https://github.com/BieremaBoyzProgramming/bbpPairings.git|v6"
        )
        self.defaultTarget = "v6"

        self.patchToApply["v6"] = [("0001-Add-CMake-build.patch", 1)]
        self.patchLevel["v6"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_CXX_FLAGS=-DOMIT_GENERATOR"]
