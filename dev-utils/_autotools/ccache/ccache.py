# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/jrosdahl/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["4.0"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.0"] = (['ac97af86679028ebc8555c99318352588ff50f515fc3a7f8ed21a8ad367e3d45'], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzsdt"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsCCACHE = False
