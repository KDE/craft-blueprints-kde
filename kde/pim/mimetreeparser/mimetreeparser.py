# SPDX-FileCopyrightText: g10 Code GmbH
# SPDX-FileContributor: Carl Schwan <carl.schwan@gnupg.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.svnTargets["master"] = "https://invent.kde.org/pim/mimetreeparser.git"
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


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
        self.subinfo.options.dynamic.buildTests = False
