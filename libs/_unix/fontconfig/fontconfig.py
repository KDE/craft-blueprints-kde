# -*- coding: utf-8 -*-
import info
from Package.MSBuildPackageBase import *
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.13.1"]:
            self.targets[ver] = f"https://www.freedesktop.org/software/fontconfig/release/fontconfig-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fontconfig-{ver}"
        self.targetDigests["2.13.1"] = (["9f0d852b39d75fc655f9f53850eb32555394f36104a044bb2b2fc9e66dbbfa7f"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Fontconfig is a library for configuring and customizing font access. "
        self.webpage = "https://www.freedesktop.org/wiki/Software/fontconfig/"
        self.patchLevel["2.13.1"] = 2
        self.defaultTarget = "2.13.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/uuid"] = None

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared"