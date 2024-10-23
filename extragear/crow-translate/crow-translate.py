# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hennadii Chernyshchyk <genaloner@gmail.com>

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Crow Translate"
        self.description = "A simple and lightweight translator that allows you to translate and speak text."
        self.webpage = "https://apps.kde.org/crow-translate"

        self.svnTargets["master"] = "https://invent.kde.org/office/crow-translate"
        for ver in ["3.0.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/crow-translate/{ver}/crow-translate-v{ver}.tar.gz"
            self.targetInstSrc[ver] = "crow-translate-v" + ver
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/crow-translate/{ver}/crow-translate-v{ver}.tar.gz.sha256"

        self.defaultTarget = "3.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtx11extras"] = None
        self.runtimeDependencies["libs/qt5/qttranslations"] = None
        self.buildDependencies["libs/qt5/qttools"] = None
        self.runtimeDependencies["libs/tesseract"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwayland"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        self.defines["appname"] = "CrowTranslate"
        self.defines["executable"] = r"bin\crow.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(crow|update-mime-database)).*")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
