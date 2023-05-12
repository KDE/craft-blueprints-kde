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
        self.svnTargets['c0bbc2f'] = 'https://github.com/dyne/frei0r.git||c0bbc2fe105c0ce1270d89863eeb804e58601bd9'
        self.defaultTarget = 'c0bbc2f'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/cairo"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/gavl"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += " -DWITHOUT_GAVL=1 "

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir()/"lib/frei0r-1", self.installDir()/"plugins/frei0r-1")
        return True

