# -*- coding: utf-8 -*-

import info
from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["4.13"] = "https://ftp.gnu.org/gnu/libtasn1/libtasn1-4.13.tar.gz"
        self.targetDigests["4.13"] = (['7e528e8c317ddd156230c4e31d082cd13e7ddeb7a54824be82632209550c8cca'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["4.13"] = "libtasn1-4.13"
        self.defaultTarget = "4.13"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-utils/msys"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        # Don't include the system aclocal files since it breaks gnulib:
        # https://lists.gnu.org/archive/html/bug-gnulib/2016-12/msg00140.html
        self.subinfo.options.configure.useDefaultAutoreconfIncludes = False

