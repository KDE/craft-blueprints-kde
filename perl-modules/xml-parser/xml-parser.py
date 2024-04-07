# -*- coding: utf-8 -*-
import info
from Package.PerlPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["libs/expat"] = None

    def setTargets(self):
        for ver in ["2.44", "2.47"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"XML-Parser-{ver}"
        self.targetDigests["2.44"] = (["ad4aae643ec784f489b956abe952432871a622d4e2b5c619e8855accbfc4d1d8"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["2.44"] = 1

        self.tags = "XML::Parser"
        self.defaultTarget = "2.47"


class Package(PerlPackageBase):
    def __init__(self, **args):
        super().__init__()
        root = CraftCore.standardDirs.craftRoot()
        self.subinfo.options.configure.args += f"EXPATINCPATH=\"{os.path.join(root, 'include')}\" EXPATLIBPATH=\"{os.path.join(root, 'lib')}\""
