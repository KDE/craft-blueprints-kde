# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.10.1"] = [("qtimageformats-everywhere-src-5.10.1-20180413.diff", 1)]
        self.patchLevel["5.10.1"] = 1
        self.patchLevel["kde/5.15"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/webp"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        super().__init__()
