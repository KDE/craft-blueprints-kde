import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quotient-im/libQuotient.git'

        for ver in ['0.7.1']:
            self.targets[ver] = 'https://github.com/quotient-im/libQuotient/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = 'libQuotient-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libQuotient-%s' % ver

        self.targetDigests['0.7.1'] = (['48b15c666528405219ff0be8f0f336405c64deb1719115af75ef099cb3f86555'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.7.1"] = [("0001-Fix-compilation-with-e2ee-on-windows.patch", 1)]

        self.defaultTarget = '0.7.1'
        self.description = "A Qt library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/olm"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
        self.subinfo.options.configure.args = "-DQuotient_ENABLE_E2EE=ON"
