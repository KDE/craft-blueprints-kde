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
        # requires gtests
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        for ver in ["0.12.0"]:
            self.targets[ver] = f"https://github.com/libjxl/libjxl/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libjxl-{ver}"
        self.targetDigests["0.12.0"] = (["03e9be69a30be4011f559da75328b6d7cea8ad921fabfbd551ce10bf45cdc992"], CraftHash.HashAlgorithm.SHA256)
        self.description = "JPEG XL image format reference implementation"
        self.defaultTarget = "0.12.0"

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

        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.args += [
                # necessary to avoid crashes
                "-DCMAKE_C_FLAGS=-DHWY_COMPILE_ONLY_SCALAR",
                "-DCMAKE_CXX_FLAGS=-DHWY_COMPILE_ONLY_SCALAR",
            ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMSVC():
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
