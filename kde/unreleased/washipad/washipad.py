# SPDX-FileCopyrightText: 2024 Laurent Montel <montel@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Washipad"
        self.description = "WashiPad is a minimalist sketchnoting application meant to be used with a graphic tablet."

        self.svnTargets["master"] = "https://invent.kde.org/graphics/washipad.git"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False

    def createPackage(self):
        self.defines["shortcuts"] = [{"name": "Washipad", "target": "bin/washipad.exe", "description": self.subinfo.description, "appId": "washipad"}]
        return super().createPackage()
