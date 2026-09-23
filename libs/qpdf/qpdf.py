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
        self.targetDigests["12.4.1"] = (["ebab3840fa8f370a1d4a1b4b7b08fad5baebeb5b5fa3cbbda88cd81e4fccecc9"], CraftHash.HashAlgorithm.SHA256)
        self.description = "C++ library that performs content-preserving transformations on PDF files"
        self.defaultTarget = "12.4.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["libs/openjpeg"] = None
        self.runtimeDependencies["libs/gnutls"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DMAINTAINER_MODE=OFF"]
