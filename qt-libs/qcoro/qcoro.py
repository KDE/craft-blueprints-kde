import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/danvratil/qcoro.git"

        for ver in ["0.9.0", "0.10.0"]:
            self.targets[ver] = "https://github.com/danvratil/qcoro/archive/refs/tags/v%s.tar.gz" % ver
            self.archiveNames[ver] = "qcoro-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "qcoro-%s" % ver

        self.targetDigests["0.9.0"] = (["cfaf6b778450f06adac4ce5e353eb6eae213a3b62b8c8740520d58cf9fe3ec1a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.10.0"] = (["b7c8f00273ad27d85814bf4ec93eb6922c75656800a61d11854d36355a4a1aec"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.10.0"
        self.description = "C++ Coroutines for Qt"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.dynamic.buildTests = False
        self.subinfo.options.configure.args = ["-DQCORO_BUILD_EXAMPLES=OFF"]
