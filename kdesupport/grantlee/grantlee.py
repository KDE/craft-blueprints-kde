# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/steveire/grantlee.git"
        self.targets["5.2.0"] = "https://github.com/steveire/grantlee/archive/v5.2.0.tar.gz"
        self.targetDigests["5.2.0"] = (['139acee5746b957bdf1327ec0d97c604d4c0b9be42aec5d584297cb5ed6a990a'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.2.0"] = "grantlee-5.2.0"
        self.defaultTarget = "5.2.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtscript"] = None # optional dep, but we probably want to have it enabled


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
