# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.9.8"] = "https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.8.tar.xz"
        self.targetDigests["0.9.8"] = (["7b9338cf52706facb2e18587dceda2fbc4a2a3519efa1e15a3f2a68193942f80"], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["0.9.8"] = "libunistring-0.9.8.tar.xz"
        self.targetInstSrc["0.9.8"] = "libunistring-0.9.8"

        self.targets["0.9.10"] = "https://ftp.gnu.org/gnu/libunistring/libunistring-0.9.10.tar.xz"
        self.targetDigests["0.9.10"] = (["eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7"], CraftHash.HashAlgorithm.SHA256)
        self.archiveNames["0.9.10"] = "libunistring-0.9.10.tar.xz"
        self.targetInstSrc["0.9.10"] = "libunistring-0.9.10"

        self.defaultTarget = "0.9.10"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
        # Don't include the system aclocal files since it breaks gnulib:
        # https://lists.gnu.org/archive/html/bug-gnulib/2016-12/msg00140.html
        self.subinfo.options.configure.useDefaultAutoreconfIncludes = False
