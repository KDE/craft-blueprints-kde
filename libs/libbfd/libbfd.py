# -*- coding: utf-8 -*-
import info
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "2.31"
        self.targets[ver] = f"https://ftp.gnu.org/gnu/binutils/binutils-{ver}.tar.bz2"
        self.targetInstSrc[ver] = f"binutils-{ver}/bfd"
        self.targetDigests[ver] = ("2c49536b1ca6b8900531b9e34f211a81caf9bf85b1a71f82b81ae32fcd8ffe19", CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.buildDependencies["dev-utils/msys"] = None


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--with-system-zlib"]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.autoreconf = False


if CraftCore.compiler.isMinGW():

    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)

else:

    class Package(VirtualPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
