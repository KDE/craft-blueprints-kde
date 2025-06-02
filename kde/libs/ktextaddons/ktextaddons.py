# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Laurent Montel <montel@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.description = "Text Addons (autocorrection, grammar checking, text to speak, translator support, AI support)"

        for ver in ["1.5.4", "1.6.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/ktextaddons/ktextaddons-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"ktextaddons-{ver}"

        # Remove unused DBus includes https://invent.kde.org/libraries/ktextaddons/-/merge_requests/11
        self.patchToApply["1.5.4"] = [("63fb82f2a83b6fb1900329c347f2b41fb39990ce.patch", 1)]
        self.patchLevel["1.5.4"] = 1

        self.svnTargets["master"] = "https://invent.kde.org/libraries/ktextaddons.git"

        self.defaultTarget = "1.6.0"

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
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
