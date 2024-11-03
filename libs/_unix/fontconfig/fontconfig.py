# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *
from Package.MSBuildPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.15.0"]:
            self.targets[ver] = f"https://www.freedesktop.org/software/fontconfig/release/fontconfig-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fontconfig-{ver}"
        self.targetDigests["2.15.0"] = (["f5f359d6332861bd497570848fcb42520964a9e83d5e3abe397b6b6db9bcaaf4"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Fontconfig is a library for configuring and customizing font access. "
        self.webpage = "https://www.freedesktop.org/wiki/Software/fontconfig/"
        self.defaultTarget = "2.15.0"

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
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
