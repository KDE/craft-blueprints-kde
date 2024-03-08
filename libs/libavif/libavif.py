# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.2"]:
            self.targets[ver] = f"https://github.com/AOMediaCodec/libavif/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libavif-{ver}"
        self.targetDigests["1.0.2"] = (["de8bf79488c5b523b77358df8b85ae69c3078e6b3f1636fc1f313f952269ad20"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for encoding and decoding .avif files"
        self.defaultTarget = "1.0.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/aom"] = None
        self.runtimeDependencies["libs/dav1d"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DAVIF_CODEC_AOM=ON", "-DAVIF_CODEC_DAV1D=ON", "-DAVIF_ENABLE_WERROR=OFF", "-DAVIF_ENABLE_GTEST=OFF"]
