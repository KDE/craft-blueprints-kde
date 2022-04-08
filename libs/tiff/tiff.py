import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a library to manipulate TIFF image files"
        self.webpage = "http://www.simplesystems.org/libtiff/"

        self.defaultTarget = '4.3.0'
        self.targets[self.defaultTarget] = "http://download.osgeo.org/libtiff/tiff-" + self.defaultTarget + ".tar.gz"
        self.targetInstSrc[self.defaultTarget] = "tiff-" + self.defaultTarget
        self.patchLevel['4.3.0'] = 1

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
        # both examples and tests can be run here
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF -DBUILD_TOOLS=OFF"
