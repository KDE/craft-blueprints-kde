# -*- coding: utf-8 -*-
import info
from Blueprints.CraftVersion import CraftVersion

import subprocess
import sys
from info import DependencyRequirementType

class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A cross-platform multimedia framework based on Qt and FFmpeg."
        self.webpage = "https://github.com/wang-bin/QtAV"
        self.displayName = "QtAV"
        self.patchToApply['1.13.0'] = [
            ("0001-Include-QSGMaterial.patch", 1),
            ("0002-Fix-install-prefix.patch", 1),
            ("0003-Add-craft-search-paths.patch", 1),
        ]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.QMakePackageBase import *


class Package(QMakePackageBase):
    def __init__(self):
        QMakePackageBase.__init__(self)

    def configureOptions(self, defines=""):
        return super().configureOptions(defines + ' "CONFIG += no-examples no-tests"')

    def install(self, options=None):
        if not super().install(options):
            return False
        if OsUtils.isWin():
            return utils.system("sdk_install.bat", cwd=self.buildDir())
        return True
