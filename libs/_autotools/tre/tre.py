import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.8.0"]:
            self.targets[ver] = f"https://laurikari.net/tre/tre-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = "tre-" + ver
        #self.targetDigests['0.8.0'] = ([''], CraftHash.HashAlgorithm.SHA256)
        self.description = "portable regex matching library"
        self.defaultTarget = '0.8.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
