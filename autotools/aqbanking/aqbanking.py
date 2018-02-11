# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["5.7.6"] = "https://www.aquamaniac.de/sites/download/download.php?package=03&release=215&file=01&dummy=aqbanking-5.7.6beta.tar.gz"
        self.targetDigests["5.7.6"] = (['f9420d8b34c2eee703a7d26dd71a849700fdb2d7372b7649a3488b5a69f55565'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["5.7.6"] = "aqbanking-5.7.6beta.tar.gz"
        self.targetInstSrc["5.7.6"] = "aqbanking-5.7.6beta"

        self.defaultTarget = "5.7.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["autotools/ktoblzcheck"] = "default"
        self.runtimeDependencies["autotools/gwenhywfar"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
        # this prevents "cannot find the library libaqhbci.la or unhandled argument libaqhbci.la"
        self.subinfo.options.make.supportsMultijob = False
