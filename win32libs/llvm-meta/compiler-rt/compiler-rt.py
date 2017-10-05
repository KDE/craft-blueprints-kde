# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests['3.7.0'] = 'b61362b409bb7909a6d11097b5f69fded061073c'

        for ver in self.svnTargets.keys() | self.targets.keys():
            self.patchToApply[ver] = [("fix_shortpath.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["win32libs/llvm-meta/clang"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
