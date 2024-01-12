# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KWeatherCore"
        self.description = "Library to facilitate retrieval of weather information including forecasts and alerts"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kweathercore"

        for ver in ["0.5"]:
            self.targets[ver] = f"https://download.kde.org/stable/kweathercore/{ver}/kweathercore-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kweathercore-{ver}"

        self.targetDigests["0.5"] = (["162c69f758f2e9b1c1ef2b8d0c54f3cee439b4171ef32632df410411d30d4d6f"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["libs/qt5/qtlocation"] = None
        else:
            self.runtimeDependencies["libs/qt6/qtpositioning"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kholidays"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
