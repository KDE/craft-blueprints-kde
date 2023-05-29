import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.6.3"]:
            self.targets[ver] = f"https://movit.sesse.net/movit-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"movit-{ver}"
        self.targetDigests["1.6.3"] = (["eb19f109ec99d6050de5267d059c7b351d3d5e39c77d43ca348a95f474a99498"], CraftHash.HashAlgorithm.SHA256)
        self.description = "High-performance, high-quality video filters for the GPU"
        self.defaultTarget = "1.6.3"

    def setDependencies(self):
        self.runtimeDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/libepoxy"] = None
        self.runtimeDependencies["libs/libpng"] = None


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.make.args += " libmovit.la "
