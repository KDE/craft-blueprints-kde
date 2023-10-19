import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.2.1"]:
            self.targets[ver] = f"https://github.com/AcademySoftwareFoundation/openexr/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openexr-{ver}"
        self.targetDigests["3.2.1"] = (["61e175aa2203399fb3c8c2288752fbea3c2637680d50b6e306ea5f8ffdd46a9b"], CraftHash.HashAlgorithm.SHA256)

        self.description = "The OpenEXR project provides the specification and reference implementation of the EXR file format, the professional-grade image storage format of the motion picture industry."
        self.defaultTarget = "3.2.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # Make sure we get a .pc, even on Windows, as we'll be looking for it
        self.subinfo.options.configure.args += ["-DOPENEXR_INSTALL_PKG_CONFIG=ON"]
