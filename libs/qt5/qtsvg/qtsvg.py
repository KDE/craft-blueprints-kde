# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.15.2"] = 2
        if CraftCore.compiler.isAndroid:
            self.patchToApply["5.15.2"] = [("optional-widget-dependency.diff", 1)]
            self.patchToApply["5.15.5"] = [("optional-widget-dependency.diff", 1)]
            self.patchToApply["kde/5.15"] = [("optional-widget-dependency.diff", 1)]
            self.patchToApply["kde/before-5.15.11-rebase"] = [("optional-widget-dependency.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
