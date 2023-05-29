# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.description = "GNU gperf is a perfect hash function generator. "
        for ver in ["3.1"]:
            self.targets[ver] = f"http://ftp.gnu.org/pub/gnu/gperf/gperf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"gperf-{ver}"

        self.defaultTarget = "3.1"


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --disable-static --enable-shared"
