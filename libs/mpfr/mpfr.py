# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.2.0"]:
            self.targets[ver] = f"https://www.mpfr.org/mpfr-{ver}/mpfr-{ver}.tar.gz"
            self.archiveNames[ver] = f"mpfr-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"mpfr-{ver}"
        self.patchToApply["4.2.0"] = [("dll.patch", 1)]

        self.targetDigests["4.2.0"] = (["f1cc1c6bb14d18f0c61cc416e083f5e697b6e0e3cf9630b9b33e8e483fc960f0"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "4.2.0"
        self.description = "The MPFR library is a C library for multiple-precision floating-point computations with correct rounding"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/texinfo"] = None
        self.runtimeDependencies["libs/libgmp"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell.useMSVCCompatEnv = True
