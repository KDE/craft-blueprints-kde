# SPDX-FileCopyrightText: g10 Code GmbH
# SPDX-FileContributor: Carl Schwan <carl.schwan@gnupg.com>
# SPDX-License-Identifier: BSD-2-Clause

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Mime parsing and viewer library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/pim/kmime"] = None
        self.runtimeDependencies["kde/pim/kmbox"] = None
        self.runtimeDependencies["kde/pim/libkleo"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
