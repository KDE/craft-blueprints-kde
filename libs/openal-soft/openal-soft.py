import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.19.1']:
            self.targets[ver] = \
                f'https://github.com/kcat/openal-soft/archive/openal-soft-{ver}.tar.gz'
            self.targetInstSrc[ver] = f'openal-soft-openal-soft-{ver}'
        self.targetDigests["1.19.1"] = (['9f3536ab2bb7781dbafabc6a61e0b34b17edd16bd6c2eaf2ae71bc63078f98c7'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'a library for audio support'
        self.defaultTarget = '1.19.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
