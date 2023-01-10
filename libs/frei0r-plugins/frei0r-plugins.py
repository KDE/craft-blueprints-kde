import info

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Compiler.All

    def setTargets(self):
        self.description = 'Minimalistic plugin API for video effects, plugins collection'
        self.webpage = 'http://frei0r.dyne.org/'
        for ver in ['1.7.0', '2.2.0']:
            self.targets[ ver ] = f"https://github.com/dyne/frei0r/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = f"frei0r-{ver}"
        self.targetDigests['1.6.1'] = (['dae0ca623c83173788ce4fc74cb67ac7e50cf33a4412ee3d33bed284da1a8437'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.7.0'] = (['6f7cf95ea2257687cc31db0ed9c9bc0eec152e953d515f346eabec048ed2b29d'], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets['master'] = 'https://github.com/dyne/frei0r.git'
        self.patchLevel['master'] = 20220128
        self.svnTargets['114a72f'] = 'https://github.com/dyne/frei0r.git||114a72f438fa04c5d12593e38dac148dbb9ce10c'
        self.defaultTarget = '2.2.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/cairo"] = None
        self.runtimeDependencies["libs/gavl"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir()/"lib/frei0r-1", self.installDir()/"plugins/frei0r-1")
        return True

