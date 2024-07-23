import info
from Package.CMakePackageBase import *
from Package.MakeFilePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "[git]https://github.com/lz4/lz4.git"
        for ver in ["1.9.4", "1.10.0"]:
            self.targets[ver] = f"https://github.com/lz4/lz4/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lz4-{ver}"
            self.archiveNames[ver] = f"lz4-{ver}.tar.gz"
            self.targetConfigurePath[ver] = "build/cmake"
        self.targetDigests["1.9.4"] = (["0b0e3aa07c8c063ddf40b082bdf7e37a1562bda40a0ff5272957f3e987e0e54b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.10.0"] = (["537512904744b35e232912055ccf8ec66d768639ff3abe5788d90d792ec5f48b"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Extremely Fast Compression algorithm"
        self.defaultTarget = "1.10.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = True
