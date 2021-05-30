# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.AutoToolsPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):

        for ver in ['4.1.0']:
            self.targets[ver] = f"https://www.mpfr.org/mpfr-current/mpfr-{ver}.tar.gz"
            self.archiveNames[ver] = f"mpfr-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpfr-{ver}"

        self.targetDigests['4.1.0'] = (['3127fe813218f3a1f0adf4e8899de23df33b4cf4b4b3831a5314f78e65ffa2d6'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = '4.1.0'
        self.description = "The MPFR library is a C library for multiple-precision floating-point computations with correct rounding"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libgmp"] = None

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)

        # Fails to configure without this
        self.subinfo.options.configure.autoreconf = False
