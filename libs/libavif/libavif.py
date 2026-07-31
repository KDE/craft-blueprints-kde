# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Daniel Novomesky <dnovomesky@gmail.com>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.2"]:
            self.targets[ver] = f"https://github.com/AOMediaCodec/libavif/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libavif-{ver}"
        self.targetDigests["1.4.2"] = (["2b645287340ba5a631d268b551dc2d72bd73ac33335962dd36dcdb6d8366921d"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Library for encoding and decoding .avif files"
        self.defaultTarget = "1.4.2"

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
        self.subinfo.options.configure.args += ["-DAVIF_CODEC_AOM=SYSTEM", "-DAVIF_LIBYUV=OFF"]
