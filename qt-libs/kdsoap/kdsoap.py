# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSoap.git"
        for ver in ["2.0.0"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSoap/releases/download/kdsoap-{ver}/kdsoap-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kdsoap-{ver}"
        self.targetDigests['2.0.0'] = (
            ['d18963104fa6f7d02b044631cddbe78f18f70e06c607af680c7ace04d6cf04ee'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.0.0"
        self.description = "A Qt-based client-side and server-side SOAP component"
        self.webpage = "http://www.kdab.com/products/kd-soap"
        self.displayName = "KDSoap"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
