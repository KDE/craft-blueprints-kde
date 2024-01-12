import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.2.2"]:
            self.targets[ver] = f"https://github.com/libsndfile/libsamplerate/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libsamplerate-{ver}"
        self.targetDigests["0.2.2"] = (["16e881487f184250deb4fcb60432d7556ab12cb58caea71ef23960aec6c0405a"], CraftHash.HashAlgorithm.SHA256)
        self.description = "an audio sample rate converter library"
        self.defaultTarget = "0.2.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args += ["-DLIBSAMPLERATE_EXAMPLES=OFF"]
