# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2019 Nicolas Fella <nicolas.fella@gmx.de>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/kpublictransport.git")
        self.description = "Library for accessing public transport data"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
