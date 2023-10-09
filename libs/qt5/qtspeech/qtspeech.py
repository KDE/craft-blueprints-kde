# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.15.0"] = 1
        self.patchLevel["kde/before-5.15.11-rebase"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        if CraftCore.compiler.isUnix:
            self.runtimeDependencies["libs/speechd"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        if CraftCore.compiler.isUnix:
            self.subinfo.options.dynamic.featureArguments += ["-speechd"]
