# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSoap.git"
        for ver in ["1.7.0", "1.9.0", "1.9.1"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSoap/releases/download/kdsoap-{ver}/kdsoap-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kdsoap-{ver}"
        self.targetDigests['1.7.0'] = (
            ['c13cd01cc576e22d51f2cd336f1473894a3c78ce5300ceaa23b20420f99234bd'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.9.0'] = (
            ['e3b9626d5cb08f41a709fa35031ce17bfdd075b7387baf14ecf8a9ca10994828'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.9.1'] = (
            ['a020ea26e91a2bcdbfa7bc631870ed07be2c583ae29114cfe72a5a94e0e93d27'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['1.7.0'] = [("kdsoap-1.6.0-20171220.diff", 1)]

        self.defaultTarget = "1.9.1"
        self.description = "A Qt-based client-side and server-side SOAP component"
        self.webpage = "http://www.kdab.com/products/kd-soap"
        self.displayName = "KDSoap"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
