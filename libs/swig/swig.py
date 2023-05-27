# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/swig/swig.git"

        for ver in ["4.1.1"]:
            self.targets[ver] = f"http://prdownloads.sourceforge.net/swig/swig-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"swig-{ver}"

        self.targetDigests["4.1.1"] = (["2af08aced8fcd65cdb5cc62426768914bedc735b1c250325203716f78e39ac9b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.1.1"
        self.description = "Simplified Wrapper and Interface Generator"
        self.displayName = "SWIG"
        self.webpage = "https://www.swig.org/"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None
        self.buildDependencies["libs/pcre"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
