# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "Texinfo is the official documentation format of the GNU project. It is used by many non-GNU projects as well."
        for ver in ["6.4"]:
            self.targets[ver] = f"http://ftp.gnu.org/gnu/texinfo/texinfo-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"texinfo-{ver}"
        self.targetDigests["6.4"] = (['3714c129e37fe4b58fa3dc2f30b6b8c867de683a5cfe74e74e6a9f7c0e9a8e77'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '6.4'



class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)