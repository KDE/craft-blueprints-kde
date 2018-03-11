# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["6.1.2"] = "https://gmplib.org/download/gmp/gmp-6.1.2.tar.bz2"
        self.targetDigests['6.1.2'] = (['5275bb04f4863a13516b2f39392ac5e272f5e1bb8057b18aec1c9b79d73d8fb2'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["6.1.2"] = "gmp-6.1.2"
        self.defaultTarget = "6.1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils-win/msys"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.configure.args = "--disable-static --enable-shared --enable-cxx "
        self.subinfo.options.useShadowBuild = False


if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
