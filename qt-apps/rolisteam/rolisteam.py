# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Renaud Guezennec <renaud@rolisteam.org>
import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Rolisteam"
        self.description = "Rolisteam is a virtual tableTop for role playing games."
        self.webpage = "https://rolisteam.org"
        self.svnTargets["stable"] = "https://invent.kde.org/rolisteam/rolisteam||stable"
        self.defaultTarget = "stable"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtimageformats"] = None
        self.runtimeDependencies["libs/qt6/qtquick3dphysics"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None
        self.runtimeDependencies["libs/qt/qtscxml"] = None
        self.runtimeDependencies["libs/qt6/qthttpserver"] = None
        self.runtimeDependencies["libs/qt6/qtquick3d"] = None
        self.runtimeDependencies["libs/qt6/qtremoteobjects"] = None
        self.runtimeDependencies["libs/qt/qttools"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True

    def createPackage(self):
        self.defines["appname"] = "rolisteam"
        self.defines["icon"] = self.sourceDir() / "resources/rolisteam/logo/rolisteam.ico"
        self.defines["shortcuts"] = [{"name" : self.subinfo.displayName, "target": "bin/rolisteam.exe"}, {"name" : "rcse", "target" : "bin/rcse.exe"}, {"name" : "dice", "target" : "bin/dice.exe"}]
        return super().createPackage()
