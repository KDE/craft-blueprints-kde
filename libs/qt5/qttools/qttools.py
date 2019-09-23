# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.11.0"] = 2

    def registerOptions(self):
        self.options.dynamic.registerOption("qdocThroughLLVM", True)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        if self.options.dynamic.qdocThroughLLVM:
            self.runtimeDependencies["libs/llvm-meta/llvm"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)

    def compile(self):
        env = {}
        if self.subinfo.options.dynamic.qdocThroughLLVM:
            env = { "LLVM_INSTALL_DIR" : CraftCore.standardDirs.craftRoot(),
                "FORCE_MINGW_QDOC_BUILD" : "1"}
        with utils.ScopedEnv(env):
            return super().compile()
