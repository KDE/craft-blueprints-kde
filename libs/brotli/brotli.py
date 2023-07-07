import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/google/brotli.git"
        for ver in ["1.0.9"]:
            self.targets[ver] = f"https://github.com/google/brotli/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"brotli-{ver}"
        self.targetDigests["1.0.9"] = (["f9e8d81d0405ba66d181529af42a3354f838c939095ff99930da6aa9cdf6fe46"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.0.9"] = [("f842c1bcf9264431cd3b15429a72b7.patch", 1)]
        self.patchLevel["1.0.9"] = 1
        self.description = "Brotli compression format"
        self.webpage = "https://github.com/google/brotli"
        self.defaultTarget = "1.0.9"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
