import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.10"]:
            self.targets[ver] = f"https://github.com/fribidi/fribidi/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "fribidi-" + ver
        self.targetDigests['1.0.10'] = (['3ebb19c4184ed6dc324d2e291d7465bc6108a20be019f053f33228e07e879c4f'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.0.10"] = [("fribidi-avoid-c2man.patch", 0)]
        self.description = "Unicode Bidirectional Algorithm"
        self.defaultTarget = '1.0.10'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

