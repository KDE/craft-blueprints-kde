# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>

import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/plasma-mobile/kweather"
        self.displayName = "KWeather"
        self.description = "Weather Forecasts"

        for ver in ["0.4"]:
            self.targets[ver] = f"https://download.kde.org/unstable/kweather/{ver}/kweather-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"kweather-{ver}"

        self.defaultTarget = "0.4"
        self.targetDigests["0.4"] = (['e2847139663eecba36b27c6e050b80235ec9fa1c82e8530b36c8f0d67e14c32c'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.4"] = [('0001-Add-CMake-option-to-not-build-the-plasmoid.patch', 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kquickcharts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/libs/kweathercore"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DBUILD_PLASMOID=OFF"

    def createPackage(self):
        self.defines["executable"] = r"bin\kweather.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(alligator|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
