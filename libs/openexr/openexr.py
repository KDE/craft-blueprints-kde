import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.5"]:
            self.targets[ver] = f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openexr-{ver}"
        self.targetDigests["2.5.5"] = (["59e98361cb31456a9634378d0f653a2b9554b8900f233450f2396ff495ea76b3"], CraftHash.HashAlgorithm.SHA256)

        self.description = "The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry."
        self.defaultTarget = "2.5.5"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # Make sure we get a .pc, even on Windows, as we'll be looking for it
        self.subinfo.options.configure.args += ["-DOPENEXR_INSTALL_PKG_CONFIG=ON"]
