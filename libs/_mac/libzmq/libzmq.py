# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.3.5"]:
            self.targets[ver] = f"https://github.com/zeromq/libzmq/releases/download/v{ver}/zeromq-{ver}.tar.gz"
            self.archiveNames[ver] = f"libzmq-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zeromq-{ver}"
        self.description = "ZeroMQ lightweight messaging kernel"
        self.defaultTarget = "4.3.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None

class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
