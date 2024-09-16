# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.33"]:
            self.targets[ver] = f"http://dist.schmorp.de/libev/Attic/libev-{ver}.tar.gz"
            self.archiveNames[ver] = f"libev-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libev-" + ver
        self.description = "Asynchronous event library"
        self.defaultTarget = "4.33"
        self.patchToApply["4.33"] = ("libev-4.33.patch", 1)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.useShadowBuild = False
        self.subinfo.options.configure.args += ["--disable-dependency-tracking"]
