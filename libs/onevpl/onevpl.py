import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.14.0"]:
            self.targets[ver] = f"https://github.com/oneapi-src/oneVPL/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpl-" + ver
        self.targetDigests["2.14.0"] = (["7c6bff1c1708d910032c2e6c44998ffff3f5fdbf06b00972bc48bf2dd9e5ac06"], CraftHash.HashAlgorithm.SHA256)
        self.description = "oneVPL Video Processing Library"
        self.defaultTarget = "2.14.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
