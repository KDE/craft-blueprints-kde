import info
from Package.CMakePackageBase import *
class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/facebook/zstd.git"
        for ver in ["1.4.5"]:
            self.targets[ver] = f"https://github.com/facebook/zstd/releases/download/v{ver}/zstd-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zstd-{ver}"
            self.targetConfigurePath[ver] = "build/cmake"
        # install the dll
        self.patchToApply["1.4.5"] = [("libzstd-1.4.5-20201026.diff", 1)]
        self.targetDigests[ver] =  (['98e91c7c6bf162bf90e4e70fdbc41a8188b9fa8de5ad840c401198014406ce9e'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'Fast real-time compression algorithm '
        self.defaultTarget = '1.4.5'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
