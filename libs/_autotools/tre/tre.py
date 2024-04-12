import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "portable regex matching library"

        for ver in ["0.8.0"]:
            self.targets[ver] = f"https://laurikari.net/tre/tre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"tre-{ver}"
            self.patchToApply[ver] = ("tre-skip-po.patch", 1)
        self.targetDigests["0.8.0"] = (["8dc642c2cde02b2dac6802cdbe2cda201daf79c4ebcbb3ea133915edf1636658"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["07e66d0"] = "https://github.com/laurikari/tre.git||07e66d07b44ae95a7a89f79c7ce1090f0f4d64db"
        self.patchToApply["07e66d0"] = ("tre-skip-po.patch", 1)

        self.svnTargets["master"] = "https://github.com/laurikari/tre.git"
        self.patchToApply["master"] = ("tre-skip-po.patch", 1)

        self.defaultTarget = "07e66d0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
