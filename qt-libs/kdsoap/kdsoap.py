# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/KDAB/KDSoap.git"
        for ver in ["2.0.0", "2.1.1"]:
            self.targets[ver] = f"https://github.com/KDAB/KDSoap/releases/download/kdsoap-{ver}/kdsoap-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"kdsoap-{ver}"
        self.targetDigests["2.0.0"] = (["d18963104fa6f7d02b044631cddbe78f18f70e06c607af680c7ace04d6cf04ee"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.1.1"] = (["aed57f6b200ddf762f5d2898f7e9228dd0700881c4491aefe4006f7fa5f5c627"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.1.1"
        self.description = "A Qt-based client-side and server-side SOAP component"
        self.webpage = "http://www.kdab.com/products/kd-soap"
        self.displayName = "KDSoap"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DKDSoap_QT6=true"]
