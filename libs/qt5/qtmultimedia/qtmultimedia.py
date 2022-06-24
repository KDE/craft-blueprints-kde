# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.15.2"] = [("0001-fix-wmf-plugin.patch", 1)]
            self.patchToApply["5.15.5"] = [("0001-fix-wmf-plugin.patch", 1)]
        self.patchLevel["5.15.2"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.dynamic.featureArguments += ["-no-gstreamer"]


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
