# -*- coding: utf-8 -*-
import info
from Package.VirtualPackageBase import SourceComponentPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "OpenCV extra modules"

        self.targetDigests["4.9.0"] = (["8952c45a73b75676c522dd574229f563e43c271ae1d5bbbd26f8e2b6bc1a4dae"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.10.0"] = (["65597f8fb8dc2b876c1b45b928bbcc5f772ddbaf97539bf1b737623d0604cba1"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv"] = None


class Package(SourceComponentPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
