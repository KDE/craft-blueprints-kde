# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["2.29"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/A/AT/ATOOMIC/Template-Toolkit-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Template-Toolkit-{ver}"
        self.targetDigests["2.29"] = (["2bddd71cf41fb805fd5234780daf53226b8e7004c623e1647ba2658113614779"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["2.29"] = 1

        self.tags = "Template"
        self.defaultTarget = "2.29"


class Package(PerlPackageBase):
    def __init__(self, **args):
        super().__init__()
