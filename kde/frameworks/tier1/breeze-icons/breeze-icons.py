# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>
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

        # Fix broken icons in qrc/rcc when SKIP_INSTALL_ICONS is enabled
        # https://invent.kde.org/frameworks/breeze-icons/-/merge_requests/430
        self.patchToApply["6.8.0"] = [("430.patch", 1)]
        self.patchLevel["6.8.0"] = 1

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Native

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
