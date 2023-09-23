# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Laurent Montel <montel@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Text Addons (autocorrection, grammar checking, text to speak, translator support)"

        for ver in ["1.5.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"ktextaddons-{ver}"

        self.targetDigests["1.5.1"] = (["a72d7c4fc9802cb96a50ad7f5668205c79566db47512029c85786e2c6519cc48"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.5.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["libs/qt/qtspeech"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
