# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "OpenCV extra modules"

        self.targetDigests["4.8.0"] = (["b4aef0f25a22edcd7305df830fa926ca304ea9db65de6ccd02f6cfa5f3357dbb"], CraftHash.HashAlgorithm.SHA256)


    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv"] = None


from Package.VirtualPackageBase import *


class Package(SourceComponentPackageBase):
    def __init__(self, **args):
        SourceComponentPackageBase.__init__(self)
