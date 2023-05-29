# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["2.006003"]:
            self.targets[ver] = f"https://search.cpan.org/CPAN/authors/id/H/HA/HAARG/Sub-Quote-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Sub-Quote-{ver}"
        self.targetDigests["2.29"] = (["be1f3a6f773f351f203cdc8f614803ac492b77d15fd68d5b1f0cd3884be18176"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Sub-Quote"
        self.defaultTarget = "2.006003"


class Package(PerlPackageBase):
    def __init__(self, **args):
        PerlPackageBase.__init__(self)
