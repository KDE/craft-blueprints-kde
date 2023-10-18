import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/danvratil/qcoro.git"

        for ver in ["0.7.0"]:
            self.targets[ver] = "https://github.com/danvratil/qcoro/archive/refs/tags/v%s.tar.gz" % ver
            self.archiveNames[ver] = "qcoro-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "qcoro-%s" % ver

        self.targetDigests["0.7.0"] = (["23ef0217926e67c8d2eb861cf91617da2f7d8d5a9ae6c62321b21448b1669210"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.7.0"] = [("0002-Revert-Build-Check-if-libatomic-is-required.patch", 1)]

        self.defaultTarget = "0.7.0"
        self.description = "C++ Coroutines for Qt"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args = ["-DQCORO_BUILD_EXAMPLES=OFF"]
