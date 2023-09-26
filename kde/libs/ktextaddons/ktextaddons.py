# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Laurent Montel <montel@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Text Addons (autocorrection, grammar checking, text to speak, translator support)"

        for ver in ["1.5.2"]:
            self.targets[ver] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"ktextaddons-{ver}"

        self.targetDigests["1.5.2"] = (["288bbb1cefb1e8b570a383c792eba5fca291c46dd0155dbc2531f0a36684a7db"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.5.2"

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
