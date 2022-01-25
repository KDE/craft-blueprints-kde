# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.patchToApply["5.12.0"] = [(".qt-5.12.0", 1)]
        self.patchToApply["5.15.2"] = [("yarrlimits5152.diff", 1), ("qqmlprofilereventlimits5152.diff", 1), ("d3d12_5152.diff", 1)]
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.15.2"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/d3dcompiler"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        if self.buildType() == "MinSizeRel":
            self.subinfo.options.dynamic.featureArguments += ["-no-feature-qml-debug"]


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
