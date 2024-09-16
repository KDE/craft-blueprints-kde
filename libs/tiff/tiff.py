import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a library to manipulate TIFF image files"
        self.webpage = "http://www.simplesystems.org/libtiff/"

        for ver in ["4.4.0"]:
            self.targets[ver] = f"http://download.osgeo.org/libtiff/tiff-{ver}.tar.gz"
            self.targetDigests[ver] = (["917223b37538959aca3b790d2d73aa6e626b688e02dcda272aec24c2f498abed"], CraftHash.HashAlgorithm.SHA256)
            self.targetInstSrc[ver] = f"tiff-{ver}"
        self.defaultTarget = "4.4.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/webp"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
