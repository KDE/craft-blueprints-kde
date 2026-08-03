# SPDX-FileCopyrightText: 2026 Sayandeep Dutta <duttasayandeep9@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Mankala - A Mancala Board Game"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["qt-libs/qxmpp"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DBUILD_TESTING=OFF",
        ]
