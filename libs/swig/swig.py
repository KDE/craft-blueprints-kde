# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/swig/swig.git"

        for ver in ["4.4.1"]:
            self.targets[ver] = f"http://prdownloads.sourceforge.net/swig/swig-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"swig-{ver}"

        self.targetDigests["4.4.1"] = (["40162a706c56f7592d08fd52ef5511cb7ac191f3593cf07306a0a554c6281fcf"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "4.4.1"
        self.description = "Simplified Wrapper and Interface Generator"
        self.displayName = "SWIG"
        self.webpage = "https://www.swig.org/"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["libs/pcre2"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
