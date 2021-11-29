# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        if CraftCore.compiler.isWindows:
            self.patchToApply["13.0.0"] = [("clang-10.0.1-20210428.diff", 1)]
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None


from Package.VirtualPackageBase import *

class Package(SourceComponentPackageBase):
    def __init__(self, **args):
        SourceComponentPackageBase.__init__(self)
