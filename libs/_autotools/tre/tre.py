import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.8.0"]:
            self.targets[ver] = f"https://laurikari.net/tre/tre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = "tre-" + ver
            self.patchToApply[ver] = ('tre-skip-po.patch', 1)
        self.targetDigests['0.8.0'] = (['8dc642c2cde02b2dac6802cdbe2cda201daf79c4ebcbb3ea133915edf1636658'], CraftHash.HashAlgorithm.SHA256)
        self.svnTargets["master"] = "https://github.com/laurikari/tre.git"
        self.patchToApply['master'] = ('tre-skip-po.patch', 1)
        self.description = "portable regex matching library"
        self.defaultTarget = 'master'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
