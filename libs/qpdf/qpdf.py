# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Tomasz Bojczuk <seelook@gmail.com>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["11.9.1"]:
            self.targets[ver] = f"https://github.com/qpdf/qpdf/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"qpdf-{ver}"
        self.targetDigests["11.9.1"] = (["98d509e29def377d90ff4a34e48e8e20865600342006bff53e489f689bbbb15d"], CraftHash.HashAlgorithm.SHA256)
        self.description = "C++ library that performs content-preserving transformations on PDF files"
        self.defaultTarget = "11.9.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DMAINTAINER_MODE=ON -DBUILD_DOC=OFF"]

