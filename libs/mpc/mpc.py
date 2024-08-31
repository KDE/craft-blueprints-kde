# SPDX-FileCopyrightText: 2024 Gabriel Barrantes <gabriel.barrantes.dev@outlook.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.1"]:
            self.targets[ver] = f"https://ftp.gnu.org/gnu/mpc/mpc-{ver}.tar.gz"
            self.archiveNames[ver] = f"mpc-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpc-{ver}"
            self.targetDigests[ver] = (["ab642492f5cf882b74aa0cb730cd410a81edcdbec895183ce930e706c1c759b8"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.3.1"
        self.description = "GNU MPC is a C library for the arithmetic of complex numbers with arbitrarily high precision and correct rounding of the result"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/texinfo"] = None
        self.runtimeDependencies["libs/libgmp"] = None
        self.runtimeDependencies["libs/mpfr"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
