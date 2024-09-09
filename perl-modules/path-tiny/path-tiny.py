# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import PerlPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["0.108"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/D/DA/DAGOLDEN/Path-Tiny-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Path-Tiny-{ver}"
        self.targetDigests["0.108"] = (["3c49482be2b3eb7ddd7e73a5b90cff648393f5d5de334ff126ce7a3632723ff5"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["0.108"] = 1

        self.tags = "Path::Tiny"
        self.defaultTarget = "0.108"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
