# SPDX-FileCopyrightText: 2026 Ian Monroe <imonroe@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/dragon-media-backend.git"
        self.description = "KDE audio library using SDL3, ffmpeg, kissfft, and C++23"
        self.webpage = "https://invent.kde.org/libraries/dragon-media-backend"

        for ver in ["0.90.1"]:
            self.targets[ver] = f"https://download.kde.org/unstable/dragon-media-backend/dragon-media-backend-{ver}.tar.xz"
            self.archiveNames[ver] = f"dragon-media-backend-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"dragon-media-backend-{ver}"

        self.targetDigests["0.90.1"] = (["accec83b29d0a55cf4f70de1bc32b3d7d876fe76c033fda94a376e9181c2d9a3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.90.1"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["qt-libs/qcoro"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["libs/libsdl3"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/kissfft"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = [
            "-DBUILD_EXAMPLES=OFF",
        ]
