# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Daniel Novomesky <dnovomesky@gmail.com>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.2.1"]:
            self.targets[ver] = f"https://github.com/AOMediaCodec/libavif/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libavif-{ver}"
        self.targetDigests["1.2.1"] = (["9c859c7c12ccb0f407511bfe303e6a7247f5f6738f54852662c6df8048daddf4"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for encoding and decoding .avif files"
        self.defaultTarget = "1.2.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/aom"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/dav1d"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DAVIF_CODEC_DAV1D=SYSTEM"]
        self.subinfo.options.configure.args += ["-DAVIF_CODEC_AOM=SYSTEM", "-DAVIF_ENABLE_GTEST=OFF", "-DAVIF_LIBYUV=OFF"]
