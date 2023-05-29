import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.1", "1.3.3", "1.3.6"]:
            self.targets[ver] = "http://downloads.xiph.org/releases/vorbis/libvorbis-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "libvorbis-" + ver
        self.targetDigests["1.3.1"] = "0874dd08699240b868b22979da4c95ae6325006b"
        self.targetDigests["1.3.3"] = "8dae60349292ed76db0e490dc5ee51088a84518b"
        self.targetDigests["1.3.6"] = (["6ed40e0241089a42c48604dc00e362beee00036af2d8b3f46338031c9e0351cb"], CraftHash.HashAlgorithm.SHA256)

        self.description = "reference implementation for the vorbis audio file format"
        self.defaultTarget = "1.3.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None


class Package(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
