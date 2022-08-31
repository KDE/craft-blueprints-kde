import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/danvratil/qcoro.git'

        for ver in ['0.3.0']:
            self.targets[ver] = 'https://github.com/danvratil/qcoro/archive/refs/tags/v%s.tar.gz' % ver
            self.archiveNames[ver] = 'qcoro-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'qcoro-%s' % ver

        self.targetDigests['0.3.0'] = (['610fcf621de0cf04597e2e308d1d22a7fce2a39eafa2d4827d1ff6c8b0e724c0'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.3.0"] = [("0001-Disable-QDBus-integration-by-default-on-Windows-Mac-.patch", 1)]
        self.patchLevel["0.3.0"] = 1

        self.defaultTarget = '0.3.0'
        self.description = "C++ Coroutines for Qt"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DQCORO_BUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF"
