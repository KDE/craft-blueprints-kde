# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.PerlPackageBase import PerlPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["dev-utils/perl"] = None
        self.runtimeDependencies["libs/expat"] = None

    def setTargets(self):
        for ver in ["2.44", "2.47"]:
            self.targets[ver] = f"https://cpan.metacpan.org/authors/id/T/TO/TODDR/XML-Parser-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"XML-Parser-{ver}"
        self.targetDigests["2.44"] = (["1ae9d07ee9c35326b3d9aad56eae71a6730a73a116b9fe9e8a4758b7cc033216"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.47"] = (["ad4aae643ec784f489b956abe952432871a622d4e2b5c619e8855accbfc4d1d8"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["2.44"] = 1
        self.patchLevel["2.47"] = 2
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.47"] = [("xml-parser-2.47-20240408.diff", 1)]

        self.tags = "XML::Parser"
        self.defaultTarget = "2.47"


class Package(PerlPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = CraftCore.standardDirs.craftRoot()
        self.subinfo.options.configure.args += f"EXPATINCPATH=\"{root / 'include')}\" EXPATLIBPATH=\"{root / 'lib'}\""
