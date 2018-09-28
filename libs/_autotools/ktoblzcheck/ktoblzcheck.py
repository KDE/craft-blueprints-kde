# -*- coding: utf-8 -*-

import info
from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["1.49"] = "http://downloads.sourceforge.net/project/ktoblzcheck/ktoblzcheck-1.49.tar.gz"
        self.targetDigests["1.49"] = (['e8971bc6689ea72b174c194bd43ba2c0b65112b0c3f9fd2371562e0c3ab57d29'], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["1.49"] = "ktoblzcheck-1.49"
        self.defaultTarget = "1.49"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
