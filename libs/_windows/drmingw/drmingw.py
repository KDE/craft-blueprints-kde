import info

from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.9.1']:
            self.targets[ver] = 'https://github.com/jrfonseca/drmingw/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'drmingw-' + ver
        self.targetDigests['0.9.1'] = (['96d2880416237ba1fd7983e08949c13bf4cc3d4599b1bccef13e6c05eddf8a1d'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Postmortem debugging tools for MinGW."
        self.defaultTarget = '0.9.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
