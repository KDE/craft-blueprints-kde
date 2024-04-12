import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/google/brotli.git"
        for ver in ["1.0.9", "1.1.0"]:
            self.targets[ver] = f"https://github.com/google/brotli/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"brotli-{ver}"
        self.targetDigests["1.0.9"] = (["f9e8d81d0405ba66d181529af42a3354f838c939095ff99930da6aa9cdf6fe46"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.1.0"] = (["e720a6ca29428b803f4ad165371771f5398faba397edf6778837a18599ea13ff"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.0.9"] = [("brotli-1.0.9-20230707.diff", 1)]
        self.patchLevel["1.0.9"] = 2
        self.description = "Brotli compression format"
        self.webpage = "https://github.com/google/brotli"
        self.defaultTarget = "1.1.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
