# -*- coding: utf-8 -*-
import subprocess
import sys

import info
from Blueprints.CraftVersion import CraftVersion
from info import DependencyRequirementType


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A cross-platform multimedia framework based on Qt and FFmpeg."
        self.webpage = "https://github.com/wang-bin/QtAV"
        self.displayName = "QtAV"
        self.patchToApply["1.13.0"] = [
            ("0001-Include-QSGMaterial.patch", 1),
            ("0004-cmake-fixes.patch", 1),
            ("0005-cmake-fix-mingw-build.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DBUILD_EXAMPLES=OFF", "-DBUILD_PLAYERS=OFF", "-DBUILD_TESTS=OFF"]
