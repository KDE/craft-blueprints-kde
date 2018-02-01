# -*- coding: utf-8 -*-

import info
from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.23.9"] = "https://github.com/p11-glue/p11-kit/releases/download/0.23.9/p11-kit-0.23.9.tar.gz"
        self.targetDigests["0.23.9"] = (['e1c1649c335107a8d33cf3762eb7f57b2d0681f0c7d8353627293a58d6b4db63'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["0.23.9"] = "p11-kit-0.23.9"
        self.defaultTarget = "0.23.9"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["win32libs/libtasn1"] = "default"
        self.buildDependencies["win32libs/libffi"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --without-trust-paths "


if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
