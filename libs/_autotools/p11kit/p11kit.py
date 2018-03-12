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
        self.buildDependencies["dev-utils/msys"] = "default"
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libtasn1"] = "default"
        self.runtimeDependencies["libs/libffi"] = "default"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared --without-trust-paths "
