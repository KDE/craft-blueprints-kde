# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies( self ):
        self.runtimeDependencies["dev-utils/perl"] = None

    def setTargets(self):
        for ver in ["0.428"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/R/RE/REHSACK/List-MoreUtils-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"List-MoreUtils-{ver}"
        self.targetDigests["0.428"] = (['713e0945d5f16e62d81d5f3da2b6a7b14a4ce439f6d3a7de74df1fd166476cc2'], CraftHash.HashAlgorithm.SHA256)
        self.tags = 'List::MoreUtils'
        self.defaultTarget = '0.428'


class Package(PerlPackageBase):
    def __init__(self, **args):
        PerlPackageBase.__init__(self)
