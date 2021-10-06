import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quotient-im/libQuotient.git'

        for ver in ['0.6.10']:
            self.targets[ver] = 'https://github.com/quotient-im/libQuotient/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = 'libQuotient-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libQuotient-%s' % ver

        self.targetDigests['0.6.10'] = (['2b6011bfec72a5b3125622f97fcc0a807e6771c91a8c73d1979f6c5e811b7b2d'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.6.10'
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
