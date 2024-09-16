# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ Header only Library for Unittest"
        self.webpage = "https://github.com/catchorg/Catch2"

        # just support one version
        for ver in ["3.4.0"]:
            self.targets[ver] = f"https://github.com/catchorg/Catch2/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"Catch2-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"Catch2-{ver}"

        # 3.4.0
        self.targetDigests["3.4.0"] = (["122928b814b75717316c71af69bd2b43387643ba076a6ec16e7882bfb2dfacbb"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
