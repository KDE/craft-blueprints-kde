# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>

import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KWeatherCore"
        self.description = "Library to facilitate retrieval of weather information including forecasts and alerts"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kweathercore"

        for ver in ["0.4"]:
            self.targets[ver] = f"https://download.kde.org/stable/kweathercore/{ver}/kweathercore-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kweathercore-{ver}"

        self.targetDigests["0.4"] = (['47aa124c045d159572d2a8a589f8fc77ee7aedcf7a0c7256a5e3f6f42bb9b195'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.4"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
