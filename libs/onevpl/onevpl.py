import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.13.0"]:
            self.targets[ver] = f"https://github.com/oneapi-src/oneVPL/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpl-" + ver
        self.targetDigests["2.13.0"] = (["1c740e2b58f7853f56b618bdb7d4a7e5d37f8c1a9b30105a0b79ba80873e1cbd"], CraftHash.HashAlgorithm.SHA256)
        self.description = "oneVPL Video Processing Library"
        self.defaultTarget = "2.13.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
