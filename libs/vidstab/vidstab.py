import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.1.0']:
            self.targets[ver] = 'https://github.com/georgmartius/vid.stab/archive/v' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'vid.stab-' + ver
        self.targetDigests['1.1.0'] = (['14d2a053e56edad4f397be0cb3ef8eb1ec3150404ce99a426c4eb641861dc0bb'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'Video stabilization library'
        self.defaultTarget = '1.1.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
