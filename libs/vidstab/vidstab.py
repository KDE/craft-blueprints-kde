import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Compiler.All

    def setTargets(self):
        for ver in ['1.1.0', '1.1.1']:
            self.targets[ver] = 'https://github.com/georgmartius/vid.stab/archive/v' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'vid.stab-' + ver
        self.targetDigests['1.1.0'] = (['14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.1.1'] = (['9001b6df73933555e56deac19a0f225aae152abbc0e97dc70034814a1943f3d4'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'Video stabilization library'
        self.defaultTarget = '1.1.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args = "-DUSE_OMP=OFF "
