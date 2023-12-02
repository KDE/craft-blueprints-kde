# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/utilities/keysmith.git")
        self.displayName = "Keysmith"
        self.description = "OTP client for Plasma Mobile and Desktop"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["libs/libsodium"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(self.packageDir() / "blacklist.txt")
        self.subinfo.options.configure.args += ["-DBUILD_EXTERNAL=OFF"]

    def createPackage(self):
        self.defines["executable"] = r"bin\keysmith.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(keysmith|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
