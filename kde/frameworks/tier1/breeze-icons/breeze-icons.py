# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>
# SPDX-FileCopyrightText: 2016 Kevin Funke <kfunk@kde.org>
# SPDX-FileCopyrightText: 2015 Hannah von Reth <vonreth@kde.org>

import os

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Breeze icon theme."

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid
        self.options.dynamic.registerOption("useBreezeDark", False)
        self.options.dynamic.registerOption("useIconResource", True)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["python-modules/lxml"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
        if self.subinfo.options.dynamic.useIconResource:
            self.subinfo.options.configure.args += ["-DBINARY_ICONS_RESOURCE=ON", "-DSKIP_INSTALL_ICONS=ON", "-DICONS_LIBRARY=ON"]

    def install(self):
        if not CraftPackageObject.get("kde").pattern.install(self):
            return False
        if self.subinfo.options.dynamic.useIconResource:
            dest = self.installDir() / os.path.relpath(CraftCore.standardDirs.locations.data, CraftCore.standardDirs.craftRoot())
            if not os.path.exists(dest):
                os.makedirs(dest)
            if not self.subinfo.options.dynamic.useBreezeDark:
                theme = self.buildDir() / "icons/breeze-icons.rcc"
            else:
                theme = self.buildDir() / "icons-dark/breeze-icons-dark.rcc"

            return utils.copyFile(theme, dest / "icontheme.rcc")
        else:
            return True
