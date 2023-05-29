import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.0"]:
            self.targets[ver] = f"https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libwebp-{ver}"
        self.targetDigests["1.3.0"] = (["64ac4614db292ae8c5aa26de0295bf1623dbb3985054cb656c55e67431def17c"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.3.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/giflib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
