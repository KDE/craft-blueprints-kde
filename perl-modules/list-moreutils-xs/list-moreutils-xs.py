# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["0.430"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-XS-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"List-MoreUtils-XS-{ver}"
        self.targetDigests["0.430"] = (["e8ce46d57c179eecd8758293e9400ff300aaf20fefe0a9d15b9fe2302b9cb242"], CraftHash.HashAlgorithm.SHA256)
        self.tags = "List::MoreUtils::XS"
        self.defaultTarget = "0.430"


class Package(PerlPackageBase):
    def __init__(self, **args):
        super().__init__()
