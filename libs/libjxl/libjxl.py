# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # this requires a proper gtest install
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        for ver in ["0.11.1"]:
            self.targets[ver] = f"https://github.com/libjxl/libjxl/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libjxl-{ver}"
        self.targetDigests["0.11.1"] = (["1492dfef8dd6c3036446ac3b340005d92ab92f7d48ee3271b5dac1d36945d3d9"], CraftHash.HashAlgorithm.SHA256)
        self.description = "JPEG XL image format reference implementation"
        self.patchLevel["0.11.1"] = 2
        self.defaultTarget = "0.11.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/brotli"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libhwy"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += [
            "-DJPEGXL_ENABLE_FUZZERS=OFF",
            "-DJPEGXL_ENABLE_TOOLS=OFF",
            "-DJPEGXL_ENABLE_JPEGLI=OFF",
            "-DJPEGXL_ENABLE_JPEGLI_LIBJPEG=OFF",
            "-DJPEGXL_ENABLE_DOXYGEN=OFF",
            "-DJPEGXL_ENABLE_MANPAGES=OFF",
            "-DJPEGXL_ENABLE_BENCHMARK=OFF",
            "-DJPEGXL_ENABLE_EXAMPLES=OFF",
            "-DJPEGXL_ENABLE_JNI=OFF",
            "-DJPEGXL_ENABLE_SJPEG=OFF",
            "-DJPEGXL_ENABLE_OPENEXR=OFF",
            "-DJPEGXL_ENABLE_SKCMS=OFF",
            "-DJPEGXL_ENABLE_TCMALLOC=OFF",
            "-DJPEGXL_FORCE_SYSTEM_BROTLI=ON",
            "-DJPEGXL_FORCE_SYSTEM_LCMS2=ON",
            "-DJPEGXL_FORCE_SYSTEM_HWY=ON",
        ]

        if CraftCore.compiler.compiler.isMinGW:
            self.subinfo.options.configure.args += [
                # necessary to avoid crashes
                "-DCMAKE_C_FLAGS=-DHWY_COMPILE_ONLY_SCALAR",
                "-DCMAKE_CXX_FLAGS=-DHWY_COMPILE_ONLY_SCALAR",
            ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.compiler.isMSVC:
            for pc in utils.filterDirectoryContent(
                self.installDir(),
                whitelist=lambda x, root: Path(x).suffix.lower() in [".pc"],
                blacklist=lambda x, root: True,
            ):
                pc = Path(pc)
                with pc.open("rt") as input:
                    content = input.read()
                with pc.open("wt") as output:
                    output.write(content.replace("-lm", ""))
        return True
