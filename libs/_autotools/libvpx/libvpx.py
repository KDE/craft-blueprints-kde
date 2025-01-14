import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "VP8 and VP9 video codec"

        for ver in ["1.13.1", "1.15.0"]:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpx-" + ver
        self.targetDigests["1.13.1"] = (["00dae80465567272abd077f59355f95ac91d7809a2d3006f9ace2637dd429d14"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.15.0"] = (["e935eded7d81631a538bfae703fd1e293aad1c7fd3407ba00440c95105d2011e"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.13.1"] = [("detect-clang.diff", 1)]
        self.patchToApply["1.15.0"] = [("detect-clang.diff", 1)]

        self.defaultTarget = "1.15.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noCacheFile = True
        self.platform = ""
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.staticArgs = Arguments()
        self.subinfo.options.configure.args += ["--disable-examples", "--disable-install-docs", "--disable-unit-tests", "--disable-avx512"]
