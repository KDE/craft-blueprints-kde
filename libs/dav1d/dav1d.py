import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.2"]:
            self.targets[ver] = f"https://code.videolan.org/videolan/dav1d/-/archive/{ver}/dav1d-{ver}.tar.bz2"
            self.targetInstSrc[ ver ] = "dav1d-" + ver
        self.targetDigests['0.9.2'] = (['0d198c4fe63fe7f0395b1b17de75b21c8c4508cd3204996229355759efa30ef8'], CraftHash.HashAlgorithm.SHA256)
        self.description = "dav1d is the fastest AV1 decoder on all platforms"
        self.defaultTarget = '0.9.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None

from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)

