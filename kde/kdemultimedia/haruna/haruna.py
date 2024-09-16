# SPDX-FileCopyrightText: 2024 George Florea Bănuș <georgefb899@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler &= CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        self.displayName = "Haruna"
        self.description = "Media player built with Qt/QML, KDE Frameworks and libmpv"
        self.svnTargets["master"] = "https://invent.kde.org/multimedia/haruna.git"
        self.defaultTarget = "1.1.1"

        for ver in ["1.1.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/haruna/haruna-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"haruna-{ver}"
            self.archiveNames[ver] = f"haruna-{ver}.tar.gz"

        self.targetDigests["1.1.1"] = (["b665d7405e0bbae195fd63ba794371563ac00c4e2efce3bafcee4237281fee55"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/unreleased/mpvqt"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["executable"] = "bin\\haruna.exe"

        self.defines["icon"] = self.blueprintDir() / "haruna.ico"

        self.defines["mimetypes"] = ["video/mkv", "video/mp4", "video/ogm", "video/avi"]
        self.defines["file_types"] = [".mkv", ".mp4", ".ogm", ".avi"]

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
