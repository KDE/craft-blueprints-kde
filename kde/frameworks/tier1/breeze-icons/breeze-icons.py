# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>
# SPDX-FileCopyrightText: 2016 Kevin Funke <kfunk@kde.org>
# SPDX-FileCopyrightText: 2015 Hannah von Reth <vonreth@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Breeze icon theme."

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["python-modules/lxml"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DSKIP_INSTALL_ICONS=ON", "-DICONS_LIBRARY=ON"]
        if CraftCore.compiler.isWindows:  # workaround for failure of generate-24px-versions.py to create any output
            self.subinfo.options.configure.args += ["-DWITH_ICON_GENERATION=OFF"]
        self.subinfo.options.unpack.keepSymlinksOnWindows = CraftVersion(self.buildTarget) > "6.2.99"
