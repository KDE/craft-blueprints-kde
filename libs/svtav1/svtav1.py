import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # fails to build in combination with lto
        self.options.dynamic.setDefault("buildTests", not CraftCore.compiler.isMinGW())

    def setTargets(self):
        for ver in ["2.1.2", "3.1.2"]:
            self.targets[ver] = f"https://gitlab.com/AOMediaCodec/SVT-AV1/-/archive/v{ver}/SVT-AV1-v{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"SVT-AV1-v{ver}"
        self.targetDigests["2.1.2"] = (["a1d95875f7539d49f7c8fdec0623fbf984804a168da6289705d53268e3b38412"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.1.2"] = (["802e9bb2b14f66e8c638f54857ccb84d3536144b0ae18b9f568bbf2314d2de88"], CraftHash.HashAlgorithm.SHA256)
        self.description = "svtav1 is an AV1-compliant software encoder library"
        self.webpage = "https://gitlab.com/AOMediaCodec/SVT-AV1"
        self.defaultTarget = "3.1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
