# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Manuel Alcaraz Zambrano <manuel@alcarazzam.dev>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Chessament"
        self.description = "Chess tournament manager"

        self.versionInfo.setDefaultValues(
            gitUrl="https://invent.kde.org/games/chessament.git"
        )
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["libs/qt/qttools"] = None

        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None

        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None

        self.runtimeDependencies["qt-libs/qcoro"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        self.runtimeDependencies["libs/bbppairings"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["shortcuts"] = [
            {
                "name": "Chessament",
                "target": "bin/chessament.exe",
                "appId": "chessament",
                "icon": self.buildDir() / "src/CHESSAMENT_ICON.ico",
            }
        ]
        self.defines["icon"] = self.buildDir() / "src/CHESSAMENT_ICON.ico"

        self.addExecutableFilter(
            r"(bin|libexec)/(?!(chessament|bbpPairings|update-mime-database|snoretoast)).*"
        )
        self.ignoredPackages.append("binary/mysql")

        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
