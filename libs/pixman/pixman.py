import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.40.0']:
            self.targets[ver] = 'http://cairographics.org/releases/pixman-' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'pixman-' + ver
        self.description = "Image processing and manipulation library"
        self.targetDigests['0.40.0'] = (['6d200dec3740d9ec4ec8d1180e25779c00bc749f94278c8b9021f5534db223fc'], CraftHash.HashAlgorithm.SHA256)
        # https://gitlab.freedesktop.org/pixman/pixman/-/commit/bd4e7a9b9e672105bda35ff736c977adbf719c6c
        self.patchToApply["0.40.0"] = [("bd4e7a9b9e672105bda35ff736c977adbf719c6c.diff", 1)]
        self.defaultTarget = '0.40.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None

from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
