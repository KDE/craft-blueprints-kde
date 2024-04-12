# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.4"]:
            self.targets[ver] = f"https://github.com/AOMediaCodec/libavif/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libavif-{ver}"
        self.targetDigests["1.0.4"] = (["dc56708c83a4b934a8af2b78f67f866ba2fb568605c7cf94312acf51ee57d146"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for encoding and decoding .avif files"
        self.defaultTarget = "1.0.4"

    def setDependencies(self):
        self.runtimeDependencies["libs/aom"] = None
        self.runtimeDependencies["libs/dav1d"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DAVIF_CODEC_AOM=ON", "-DAVIF_CODEC_DAV1D=ON", "-DAVIF_ENABLE_WERROR=OFF", "-DAVIF_ENABLE_GTEST=OFF"]
