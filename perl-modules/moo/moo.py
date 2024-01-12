# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["2.003006"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/H/HA/HAARG/Moo-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Moo-{ver}"
        self.targetDigests["2.29"] = (["bcb2092ab18a45005b5e2e84465ebf3a4999d8e82a43a09f5a94d859ae7f2472"], CraftHash.HashAlgorithm.SHA256)

        self.tags = "Moo"
        self.defaultTarget = "2.003006"


class Package(PerlPackageBase):
    def __init__(self, **args):
        super().__init__()
