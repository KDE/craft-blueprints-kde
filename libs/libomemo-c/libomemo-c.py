# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildStatic", CraftCore.compiler.isWindows)

    def setDependencies(self):
        self.buildDependencies["libs/libprotobuf-c"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/dino/libomemo-c.git"
        self.defaultTarget = "0.5.1"
        self.targets[self.defaultTarget] = f"https://github.com/dino/libomemo-c/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"libomemo-c-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"libomemo-c-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (["d1b65dbf7bccc67523abfd5e429707f540b2532932d128b2982f0246be2b22a0"], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://github.com/dino/libomemo-c"
        self.releaseManagerId = 359676


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
