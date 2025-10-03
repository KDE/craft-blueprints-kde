# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
import utils
from CraftCore import CraftCore
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings generator to create Python wrapper"
        self.defaultTarget = "6.9.2"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowPrebuildBinaries = True
        self.subinfo.options.configure.args += ["-v", "-v", "-v"]

    def install(self):
        if not super().install():
            return False

        # utils.createSymlink(CraftCore.standardDirs.craftRoot() / "lib/python3.11/site-packages/PySide6", CraftCore.standardDirs.craftRoot() / "share/PySide6")

        return True
