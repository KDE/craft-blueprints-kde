# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
import utils
from CraftCore import CraftCore
from Package.SourceOnlyPackageBase import SourceOnlyPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/Bartoloni/RustedBronze.git"
        self.svnTargets["e748059"] = "https://github.com/Bartoloni/RustedBronze.git||e748059b2c28915c0fff70b8d5027d75708edbb8"

        self.defaultTarget = "e748059"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(SourceOnlyPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if CraftCore.compiler.isWindows:
            destDir = self.installDir() / "bin/data/color-schemes"
        else:
            destDir = self.installDir() / "share/color-schemes"

        return utils.globCopyDir(self.sourceDir(), destDir, ["*.colors"], linkOnly=False)
