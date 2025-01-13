# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildStatic", CraftCore.compiler.isWindows)

    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/dino/libomemo-c.git|omemo"
        self.defaultTarget = "0.5.0"
        self.targets[self.defaultTarget] = f"https://github.com/dino/libomemo-c/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"libomemo-c-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"libomemo-c-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (["03195a24ef7a86c339cdf9069d7f7569ed511feaf55e853bfcb797d2698ba983"], CraftHash.HashAlgorithm.SHA256)


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
