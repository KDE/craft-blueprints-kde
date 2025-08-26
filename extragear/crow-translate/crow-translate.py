# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hennadii Chernyshchyk <genaloner@gmail.com>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Crow Translate"
        self.description = "A simple and lightweight translator that allows you to translate and speak text."
        self.webpage = "https://apps.kde.org/crow-translate"
        self.svnTargets["master"] = "https://invent.kde.org/office/crow-translate.git|master"
        for ver in ["4.0.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/crow-translate/{ver}/crow-translate-v{ver}.tar.gz"
            self.targetInstSrc[ver] = "crow-translate-v" + ver
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/crow-translate/{ver}/crow-translate-v{ver}.tar.gz.sha256"
        self.defaultTarget = "4.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt/qtscxml"] = None
        self.runtimeDependencies["libs/qt/qtspeech"] = None
        self.runtimeDependencies["libs/qt/qttranslations"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/tesseract"] = None
        self.runtimeDependencies["kde/plasma/kwayland"] = None
        if not CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/onnxruntime"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        self.defines["appname"] = "CrowTranslate"
        self.defines["executable"] = r"bin\crow.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(crow|update-mime-database)).*")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
