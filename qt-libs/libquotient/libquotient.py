import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quotient-im/libQuotient.git'

        for ver in ['0.6.11']:
            self.targets[ver] = 'https://github.com/quotient-im/libQuotient/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = 'libQuotient-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libQuotient-%s' % ver

        self.patchToApply['0.6.11'] = [('0001-Use-GNUInstallDirs-also-on-Windows.patch', 1)]
        self.patchLevel['0.6.11'] = 1

        self.targetDigests['0.6.11'] = (['12b15d1296e630477d5e8f4d32c821dc724b3c5b99d15d383417ba7d88f03c46'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.6.11'
        self.description = "A Qt5 library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
