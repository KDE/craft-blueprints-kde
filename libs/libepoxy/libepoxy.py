import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.5.9"]:
            self.targets[ver] = f"https://github.com/anholt/libepoxy/releases/download/{ver}/libepoxy-{ver}.tar.xz"
            self.targetInstSrc[ ver ] = "libepoxy-" + ver
        self.targetDigests['1.5.9'] = (['d168a19a6edfdd9977fef1308ccf516079856a4275cf876de688fb7927e365e4'], CraftHash.HashAlgorithm.SHA256)
        self.description = "library for handling OpenGL function pointer management for you"
        self.defaultTarget = '1.5.9'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None

from Package.MesonPackageBase import *


class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)

