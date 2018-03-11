# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['2.21.1a'] = "http://ftp.gnu.org/gnu/binutils/binutils-2.21.1a.tar.bz2"
        self.targetInstSrc['2.21.1a'] = 'binutils-2.21.1/bfd'
        self.targetDigests['2.21.1a'] = '525255ca6874b872540c9967a1d26acfbc7c8230'
        self.defaultTarget = '2.21.1a'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["dev-util/msys"] = "default"


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMinGW(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)


if CraftCore.compiler.isMinGW():
    class Package(PackageMinGW):
        def __init__(self):
            PackageMinGW.__init__(self)
else:
    class Package(VirtualPackageBase):
        def __init__(self):
            VirtualPackageBase.__init__(self)
