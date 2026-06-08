import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildTools", not CraftCore.compiler.isAndroid)

    def setTargets(self):
        self.description = "a library to manipulate TIFF image files"
        self.webpage = "http://www.simplesystems.org/libtiff/"

        for ver in ["4.7.1"]:
            self.targets[ver] = f"http://download.osgeo.org/libtiff/tiff-{ver}.tar.gz"
            self.targetDigests[ver] = (["f698d94f3103da8ca7438d84e0344e453fe0ba3b7486e04c5bf7a9a3fabe9b69"], CraftHash.HashAlgorithm.SHA256)
            self.targetInstSrc[ver] = f"tiff-{ver}"
        self.defaultTarget = "4.7.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/webp"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            f"-Dtiff-tools={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-Dtiff-tests={self.subinfo.options.dynamic.buildTests.asOnOff}",
            f"-Dtiff-contrib={CraftCore.compiler.isAndroid.inverted.asOnOff}",
        ]
