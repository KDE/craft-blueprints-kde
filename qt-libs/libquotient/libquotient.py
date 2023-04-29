import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/quotient-im/libQuotient.git'

        for ver in ['0.7.2']:
            self.targets[ver] = 'https://github.com/quotient-im/libQuotient/archive/%s.tar.gz' % ver
            self.archiveNames[ver] = 'libQuotient-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'libQuotient-%s' % ver

        self.targetDigests['0.7.2'] = (['62ff42c8fe321e582ce8943417c1d815ab3f373a26fa0d99a5926e713f6a9382'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.7.2'
        self.description = "A Qt library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if self.options.dynamic.buildWithQt6:
            self.runtimeDependencies["libs/qt6/qtbase"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtbase"] = None
            self.runtimeDependencies["libs/qt5/qtmultimedia"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/olm"] = None

    def registerOptions(self):
        self.options.dynamic.registerOption("buildWithQt6", False)


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
        self.subinfo.options.configure.args = "-DQuotient_ENABLE_E2EE=ON"
        if self.subinfo.options.dynamic.buildWithQt6:
            self.subinfo.options.configure.args = "-DBUILD_WITH_QT6=1"
