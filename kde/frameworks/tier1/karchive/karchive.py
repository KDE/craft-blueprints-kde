# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <julius.kuenzel@kde.org>
# SPDX-FileCopyrightText: 2016 Hannah von Reth <vonreth@kde.org>
# SPDX-FileCopyrightText: 2015 Kevin Funke <kfunk@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Qt 5 addon providing access to numerous types of archives"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/libarchive"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DWITH_BZIP2=" + ("ON" if self.subinfo.options.isActive("libs/libbzip2") else "OFF")]
        self.subinfo.options.configure.args += ["-DWITH_LIBLZMA=" + ("ON" if self.subinfo.options.isActive("libs/liblzma") else "OFF")]
        self.subinfo.options.configure.args += ["-DWITH_LIBZSTD=" + ("ON" if self.subinfo.options.isActive("libs/libzstd") else "OFF")]
