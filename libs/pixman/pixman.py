import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.40.0']:
            self.targets[ver] = 'http://cairographics.org/releases/pixman-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'pixman-' + ver
        self.targetDigests['0.40.0'] = (['6d200dec3740d9ec4ec8d1180e25779c00bc749f94278c8b9021f5534db223fc'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.40.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None

from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
