# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.18.3"]:
            self.targets[ver] = f"https://gitlab.freedesktop.org/fontconfig/fontconfig/-/archive/{ver}/fontconfig-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"fontconfig-{ver}"
        self.targetDigests["2.18.3"] = (["8d28f79d2017cbe1fbb7da84b2502c86421b4f45860234d2f4ab5b35564c8d01"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Fontconfig is a library for configuring and customizing font access. "
        self.webpage = "https://www.freedesktop.org/wiki/Software/fontconfig/"
        self.defaultTarget = "2.18.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/expat"] = None
        self.runtimeDependencies["libs/uuid"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__(**args)
