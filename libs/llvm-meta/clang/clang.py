# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/llvm-meta/llvm"] = None


from Package.VirtualPackageBase import *

class Package(SourceComponentPackageBase):
    def __init__(self, **args):
        SourceComponentPackageBase.__init__(self)
