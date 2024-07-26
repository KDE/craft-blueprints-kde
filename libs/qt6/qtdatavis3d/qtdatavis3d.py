# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Qt 3D data visualization framework"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None


from Package.CMakePackageBase import *

class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)