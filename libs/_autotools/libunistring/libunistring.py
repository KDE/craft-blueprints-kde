# -*- coding: utf-8 -*-

# Copyright (C) 2018 Łukasz Wojniłowicz <lukasz.wojnilowicz@gmail.com>

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.10", "1.2"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/libunistring/libunistring-{ver}.tar.xz"
            self.archiveNames[ver] = f"libunistring-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libunistring-{ver}"
        self.targetDigests["0.9.10"] = (["eb8fb2c3e4b6e2d336608377050892b54c3c983b646c561836550863003c05d7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.2"] = (["632bd65ed74a881ca8a0309a1001c428bd1cbd5cd7ddbf8cedcd2e65f4dcdc44"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
