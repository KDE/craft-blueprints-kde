# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.3.6"]:
            self.targets[ver] = f"https://github.com/knro/libzmq/archive/refs/tags/{ver}.tar.gz"
            self.archiveNames[ver] = f"libzmq-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libzmq-{ver}"
        self.description = "ZeroMQ lightweight messaging kernel"
        self.defaultTarget = "4.3.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
