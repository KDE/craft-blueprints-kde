import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/danvratil/qcoro.git'

        for ver in ['0.6.0']:
            self.targets[ver] = 'https://github.com/danvratil/qcoro/archive/refs/tags/v%s.tar.gz' % ver
            self.archiveNames[ver] = 'qcoro-%s.tar.gz' % ver
            self.targetInstSrc[ver] = 'qcoro-%s' % ver

        self.targetDigests['0.6.0'] = (['26d6ea1103c51b895e93d27b59bee394f80db8fd9ca21e7c0056583b1938906d'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '0.6.0'
        self.description = "C++ Coroutines for Qt"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DQCORO_BUILD_EXAMPLES=OFF -DBUILD_TESTING=OFF"
