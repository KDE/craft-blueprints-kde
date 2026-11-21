# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
import utils
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.architecture = CraftCore.compiler.Architecture.arm64

    def setTargets(self):
        self.description = "Perl script that implements a subset of the GNU as preprocessor that Apple's as doesn't."
        self.svnTargets["master"] = "https://github.com/FFmpeg/gas-preprocessor.git"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["dev-utils/perl"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        return utils.copyFile(self.sourceDir() / "gas-preprocessor.pl", self.installDir() / "bin/gas-preprocessor.pl")
