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
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "


if CraftCore.compiler.isMinGW() or CraftCore.compiler.isGCCLike:
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
