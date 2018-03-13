import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['4.0', '4.1', '4.2.1']:
            self.targets[ver] = 'http://downloads.sourceforge.net/libmsn/libmsn-' + ver + '.tar.bz2'
            self.targetInstSrc[ver] = 'libmsn-' + ver
        self.patchToApply['4.0'] = ('libmsn-4.0-20101012.diff', 1)
        self.patchToApply['4.1'] = ('libmsn-4.1-20101012.diff', 1)
        self.patchToApply['4.2.1'] = ('libmsn-4.1-20101012.diff', 1)

        self.description = "a library for connecting to Microsoft's MSN Messenger service"
        self.defaultTarget = '4.2.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/openssl"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
