import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.16.0']:
            self.targets[ver] = 'http://cairographics.org/releases/cairo-' + ver + '.tar.xz'
            self.targetInstSrc[ver] = 'cairo-' + ver
        self.targetDigests['1.16.0'] = (['5e7b29b3f113ef870d1e3ecf8adf21f923396401604bda16d44be45e66052331'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Multi-platform 2D graphics library"
        self.defaultTarget = '1.16.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/pixman"] = None

from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
