# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["libs/gettext"] = "default"
        self.runtimeDependencies["libs/expat"] = "default"
        self.runtimeDependencies["libs/tiff"] = "default"
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
