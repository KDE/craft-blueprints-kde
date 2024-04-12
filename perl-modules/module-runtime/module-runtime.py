# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["0.016"]:
            self.targets[ver] = f"https://search.cpan.org/CPAN/authors/id/Z/ZE/ZEFRAM/Module-Runtime-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Module-Runtime-{ver}"
        self.targetDigests["2.29"] = (["68302ec646833547d410be28e09676db75006f4aa58a11f3bdb44ffe99f0f024"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Module-Runtime"
        self.defaultTarget = "0.016"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
