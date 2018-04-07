# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        if CraftCore.compiler.isMinGW():
            self.patchToApply["5.0.1"] = [("0501-fixes-to-get-lldb-building.patch", 1)]#https://github.com/Alexpux/MINGW-packages/blob/5cbc0add24760165f557fd00bd9d915279ea4611/mingw-w64-clang/0501-fixes-to-get-lldb-building.patch
            self.patchToApply["6.0.0"] = [("0501-fixes-to-get-lldb-building.patch", 1)]#https://github.com/Alexpux/MINGW-packages/blob/5cbc0add24760165f557fd00bd9d915279ea4611/mingw-w64-clang/0501-fixes-to-get-lldb-building.patch


    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/llvm-meta/llvm"] = "default"


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self, **args):
        SourceOnlyPackageBase.__init__(self)
