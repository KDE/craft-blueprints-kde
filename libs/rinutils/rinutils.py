# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A C11 / gnu11 utilities C library"
        self.webpage = "https://github.com/shlomif/rinutils/"

        # just support one version
        ver = "0.8.0"
        self.defaultTarget = ver
        self.targets[ver] = f"https://github.com/shlomif/rinutils/releases/download/{ver}/rinutils-{ver}.tar.xz"
        self.archiveNames[ver] = f"rinutils-{ver}.tar.xz"
        self.targetInstSrc[ver] = f"rinutils-{ver}"
        self.targetDigests[ver] = (["1d9677cdfb2792436db993aeff7e8e91670d5c4deae62b70ec82d452615409e0"], CraftHash.HashAlgorithm.SHA256)


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
