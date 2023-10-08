# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.15.2"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["5.15.5"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/5.15"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["kde/before-5.15.11-rebase"] = [("0001-fix-wmf-plugin.patch", 1)]
        self.patchLevel["5.15.2"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.dynamic.featureArguments += ["-no-gstreamer"]
