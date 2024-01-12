# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):

        for ver in ["2.0.2"]:
            self.targets[ver] = f"https://sparsehash.googlecode.com/files/sparsehash-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"sparsehash-{ver}"

        self.targetDigests["2.0.2"] = "12c7552400b3e20464b3362286653fc17366643e"

        self.description = "An extremely memory-efficient hash_map implementation."
        self.webpage = "https://code.google.com/p/sparsehash/"
        self.defaultTarget = "2.0.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
