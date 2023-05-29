import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a library to manipulate TIFF image files"
        self.webpage = "http://www.simplesystems.org/libtiff/"

        self.defaultTarget = "4.4.0"
        self.targets[self.defaultTarget] = "http://download.osgeo.org/libtiff/tiff-" + self.defaultTarget + ".tar.gz"
        self.targetDigests[self.defaultTarget] = (["917223b37538959aca3b790d2d73aa6e626b688e02dcda272aec24c2f498abed"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc[self.defaultTarget] = "tiff-" + self.defaultTarget

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/webp"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
