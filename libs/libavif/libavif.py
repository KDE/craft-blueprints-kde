# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Daniel Novomesky <dnovomesky@gmail.com>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.0"]:
            self.targets[ver] = f"https://github.com/AOMediaCodec/libavif/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libavif-{ver}"
        self.targetDigests["1.3.0"] = (["0a545e953cc049bf5bcf4ee467306a2f113a75110edf59e61248873101cd26c1"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for encoding and decoding .avif files"
        self.defaultTarget = "1.3.0"

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
