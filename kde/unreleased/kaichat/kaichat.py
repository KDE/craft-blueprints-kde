# SPDX-FileCopyrightText: 2025 by Laurent Montel <montel@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KAIChat"
        self.description = "Chat with AI"

        for ver in ["0.4.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kaichat/kaichat-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kaichat/kaichat-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"kaichat-{ver}"

        self.svnTargets["master"] = "https://invent.kde.org/utilities/kaichat.git"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kstatusnotifieritem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/libs/ktextaddons"] = None
        self.runtimeDependencies["libs/kdsingleapplication"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/unreleased/kaichat-addons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["shortcuts"] = [{"name": "KAIChat", "target": "bin/kaichat.exe", "description": self.subinfo.description, "appId": "kaichat"}]
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["alias"] = "kaichat"
        self.defines["icon"] = self.blueprintDir() / "kaichat.ico"
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-kaichat.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-kaichat.png"

        if CraftCore.compiler.isMacOS:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
