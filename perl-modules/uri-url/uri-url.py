# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["1.76"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/O/OA/OALDERS/URI-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"URI-{ver}"
        self.targetDigests["1.76"] = (["b2c98e1d50d6f572483ee538a6f4ccc8d9185f91f0073fd8af7390898254413e"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.76"] = 1

        self.tags = "URI::URL"
        self.defaultTarget = "1.76"


class Package(PerlPackageBase):
    def __init__(self, **args):
        super().__init__()
