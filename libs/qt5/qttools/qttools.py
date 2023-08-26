# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.11.0"] = 2

    def registerOptions(self):
        self.options.dynamic.registerOption("qdocThroughLLVM", False)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        if self.options.dynamic.qdocThroughLLVM:
            self.runtimeDependencies["libs/llvm"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def compile(self):
        env = {}
        if self.subinfo.options.dynamic.qdocThroughLLVM:
            env = {"LLVM_INSTALL_DIR": CraftCore.standardDirs.craftRoot(), "FORCE_MINGW_QDOC_BUILD": "1"}
        with utils.ScopedEnv(env):
            return super().compile()
