import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.10"]:
            self.targets[ver] = f"https://github.com/fribidi/fribidi/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "fribidi-" + ver
        self.targetDigests['1.0.10'] = (['3ebb19c4184ed6dc324d2e291d7465bc6108a20be019f053f33228e07e879c4f'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.0.10"] = 1
        self.description = "Unicode Bidirectional Algorithm"
        self.defaultTarget = '1.0.10'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None

from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += "-Ddocs=false"

