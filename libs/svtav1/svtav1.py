import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # this requires a proper gtest install
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        for ver in ["v2.1.2"]:
            self.targets[ver] = f"https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/{ver}/SVT-AV1-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"SVT-AV1-{ver}"
        self.targetDigests["v2.1.2"] = (["a1d95875f7539d49f7c8fdec0623fbf984804a168da6289705d53268e3b38412"], CraftHash.HashAlgorithm.SHA256)
        self.description = "svtav1 is an AV1-compliant software encoder library"
        self.defaultTarget = "v2.1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
