# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
