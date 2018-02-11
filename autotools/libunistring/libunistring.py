# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):

        self.targets["0.9.8"] = "https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.8.tar.xz"
        self.targetDigests["0.9.8"] = (['7b9338cf52706facb2e18587dceda2fbc4a2a3519efa1e15a3f2a68193942f80'], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["0.9.8"] = "libunistring-0.9.8.tar.xz"
        self.targetInstSrc["0.9.8"] = "libunistring-0.9.8"

        self.defaultTarget = "0.9.8"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-util/msys"] = "default"

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "
