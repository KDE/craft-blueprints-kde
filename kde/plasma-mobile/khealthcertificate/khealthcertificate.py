# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Nicolas Fella <nicolas.fella@gmx.de>

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/pim/khealthcertificate.git")
        self.displayName = "KHealthCertificate"

        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DQT_MAJOR_VERSION=6"]
