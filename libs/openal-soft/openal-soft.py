import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.15.1', '1.18.0']:
            self.targets[ver] = \
                'http://kcat.strangesoft.net/openal-releases/openal-soft-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'openal-soft-' + ver
        self.patchToApply['1.15.1'] = ('openal-soft-1.15.1-20130411.diff', 1)
        self.targetDigests['1.15.1'] = 'a0e73a46740c52ccbde38a3912c5b0fd72679ec8'
        self.description = 'a library for audio support'
        self.defaultTarget = '1.18.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
