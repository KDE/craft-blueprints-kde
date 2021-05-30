# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>

import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KWeatherCore"
        self.description = "Library to facilitate retrieval of weather information including forecasts and alerts"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kweathercore"

        for ver in ["21.05"]:
            self.targets[ver] = f"https://invent.kde.org/libraries/kweathercore/-/archive/v{ver}/kweathercore-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kweathercore-v{ver}"

        self.targetDigests["21.05"] = (['f599f93d30eaa9e49c76aacef2c9b9d92cc0aa4a0cbf946c459530b149972fe1'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "21.05"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
