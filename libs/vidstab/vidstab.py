import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        for ver in ["1.1.1"]:
            self.targets[ver] = f"https://github.com/georgmartius/vid.stab/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"vid.stab-{ver}"
        self.targetDigests["1.1.1"] = (["9001b6df73933555e56deac19a0f225aae152abbc0e97dc70034814a1943f3d4"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Video stabilization library"
        self.defaultTarget = "1.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
