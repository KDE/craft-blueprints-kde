# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/utilities/keysmith.git")
        self.displayName = "Keysmith"
        self.description = "OTP client for Plasma Mobile and Desktop"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/prison"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["libs/libsodium"] = None
        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.subinfo.options.configure.args += ["-DBUILD_EXTERNAL=OFF"]

    def createPackage(self):
        self.defines["executable"] = r"bin\keysmith.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(keysmith|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.platform.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
