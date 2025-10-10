# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4", "1.5.2"]:
            self.targets[ver] = f"https://ftp.osuosl.org/pub/xiph/releases/opus/opus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"opus-{ver}"

        self.targetDigests["1.4"] = (["c9b32b4253be5ae63d1ff16eea06b94b5f0f2951b7a02aceef58e3a3ce49c51f"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Opus codec library"
        self.defaultTarget = "1.5.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
