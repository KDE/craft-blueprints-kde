# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.11.0"] = 2

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/llvm-meta/llvm"] = "default"


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)

    def compile(self):
        with utils.ScopedEnv({
            "LLVM_INSTALL_DIR" : CraftCore.standardDirs.craftRoot(),
            "FORCE_MINGW_QDOC_BUILD" : "1"}):
            return super().compile()
