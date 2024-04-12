# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["perl-modules/exporter-tiny"] = None
        self.runtimeDependencies["perl-modules/list-moreutils-xs"] = None

    def setTargets(self):
        for ver in ["0.428", "0.430"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"List-MoreUtils-{ver}"
        self.targetDigests["0.428"] = (["713e0945d5f16e62d81d5f3da2b6a7b14a4ce439f6d3a7de74df1fd166476cc2"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.430"] = (["63b1f7842cd42d9b538d1e34e0330de5ff1559e4c2737342506418276f646527"], CraftHash.HashAlgorithm.SHA256)
        self.tags = "List::MoreUtils"
        self.defaultTarget = "0.430"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
