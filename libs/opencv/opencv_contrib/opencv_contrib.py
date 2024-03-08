# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import SourceComponentPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "OpenCV extra modules"

        self.targetDigests["4.8.0"] = (["b4aef0f25a22edcd7305df830fa926ca304ea9db65de6ccd02f6cfa5f3357dbb"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv"] = None


class Package(SourceComponentPackageBase):
    def __init__(self, **args):
        super().__init__()
