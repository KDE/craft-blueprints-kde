# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["1.002002"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/T/TO/TOBYINK/Exporter-Tiny-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"Exporter-Tiny-{ver}"
        self.targetDigests["1.002002"] = (["00f0b95716b18157132c6c118ded8ba31392563d19e490433e9a65382e707101"], CraftHash.HashAlgorithm.SHA256)
        self.tags = "Exporter::Tiny"
        self.defaultTarget = "1.002002"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
