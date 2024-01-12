import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.31"]:
            self.targets[ver] = f"https://github.com/libsndfile/libsndfile/releases/download/{ver}/libsndfile-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libsndfile-{ver}"
        self.targetDigests["1.0.31"] = (["a8cfb1c09ea6e90eff4ca87322d4168cdbe5035cb48717b40bf77e751cc02163"], CraftHash.HashAlgorithm.SHA256)
        self.description = "A C library for reading and writing files containing sampled sound"
        self.defaultTarget = "1.0.31"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None
        self.runtimeDependencies["libs/libvorbis"] = None

        self.patchLevel["1.0.31"] = 1


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        # self.subinfo.options.configure.args += ["-DENABLE_COMPATIBLE_LIBSNDFILE_NAME=ON"]
