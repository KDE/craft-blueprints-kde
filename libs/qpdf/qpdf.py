# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Tomasz Bojczuk <seelook@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["12.4.1"]:
            self.targets[ver] = f"https://github.com/qpdf/qpdf/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qpdf-{ver}"
        self.targetDigests["12.4.1"] = (["f045aa277be2356ff53a89a8622945958291177d2483afc20ede7c8a8cd3873c"], CraftHash.HashAlgorithm.SHA256)
        self.description = "C++ library that performs content-preserving transformations on PDF files"
        self.defaultTarget = "12.4.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DMAINTAINER_MODE=OFF"]
