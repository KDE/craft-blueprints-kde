import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.21.1"]:
            self.targets[ver] = f"https://github.com/kcat/openal-soft/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openal-soft-{ver}"
        self.targetDigests["1.21.1"] = (["8ac17e4e3b32c1af3d5508acfffb838640669b4274606b7892aa796ca9d7467f"], CraftHash.HashAlgorithm.SHA256)
        self.description = "a library for audio support"
        self.defaultTarget = "1.21.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DALSOFT_EXAMPLES=OFF"]
