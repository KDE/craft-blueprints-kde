# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.1", "1.4"]:
            self.targets[ver] = f"https://ftp.osuosl.org/pub/xiph/releases/opus/opus-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"opus-{ver}"

        if CraftCore.compiler.isMinGW():
            self.patchToApply["1.3.1"] = [
                ("libopus-1.3.1-20220324.diff", 1)
            ]  # https://github.com/msys2/MINGW-packages/blob/7c67d9c46554d10276b2017bcfd0290dfe24a1bf/mingw-w64-opus/PKGBUILD#L36

        self.targetDigests["1.3.1"] = (["65b58e1e25b2a114157014736a3d9dfeaad8d41be1c8179866f144a2fb44ff9d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.4"] = (["c9b32b4253be5ae63d1ff16eea06b94b5f0f2951b7a02aceef58e3a3ce49c51f"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Opus codec library"
        self.defaultTarget = "1.4"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
