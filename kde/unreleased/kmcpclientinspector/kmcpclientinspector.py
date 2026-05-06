# SPDX-FileCopyrightText: 2026 by Laurent Montel <montel@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KMCpClientInspector"
        self.description = "MCP client inspector"

        self.svnTargets["master"] = "https://invent.kde.org/sdk/kmcpclientinspector.git"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["shortcuts"] = [{"name": "KMCpClientInspector", "target": "bin/kmcpclientinspector.exe", "description": self.subinfo.description, "appId": "kmcpclientinspector"}]
        self.defines["alias"] = "kmcpclientinspector"

        if CraftCore.compiler.isMacOS:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
