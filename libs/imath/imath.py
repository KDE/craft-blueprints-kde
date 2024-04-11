import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.1.11"]:
            self.targets[ver] = f"https://github.com/AcademySoftwareFoundation/Imath/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Imath-{ver}"
        self.targetDigests["3.1.11"] = (["9057849585e49b8b85abe7cc1e76e22963b01bfdc3b6d83eac90c499cd760063"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Library of 2D and 3D vector, matrix, and math operations"
        self.defaultTarget = "3.1.11"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
