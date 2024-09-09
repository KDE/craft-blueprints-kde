# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/zlib"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/stachenov/quazip"
        for ver in ["1.1", "1.4"]:
            self.targets[ver] = f"https://github.com/stachenov/quazip/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"quazip-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"quazip-{ver}"
        self.targetDigests["1.1"] = (["54edce9c11371762bd4f0003c2937b5d8806a2752dd9c0fd9085e90792612ad0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4"] = (["79633fd3a18e2d11a7d5c40c4c79c1786ba0c74b59ad752e8429746fe1781dd6"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.4"

        self.description = "Qt/C++ wrapper over minizip"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
