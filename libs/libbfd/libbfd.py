# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        version = "2.31"
        self.targets[version] = "http://ftp.gnu.org/gnu/binutils/binutils-%s.tar.bz2" % version
        self.targetInstSrc[version] = "binutils-%s/bfd" % version
        self.targetDigests[version] = ("2c49536b1ca6b8900531b9e34f211a81caf9bf85b1a71f82b81ae32fcd8ffe19", CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = version

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.buildDependencies["dev-utils/msys"] = None


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args = "--with-system-zlib "
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.autoreconf = False


if CraftCore.compiler.isMinGW():

    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)

else:

    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
