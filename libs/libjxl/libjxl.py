# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>
from pathlib import Path

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.11.1"]:
            self.svnTargets[ver] = f"https://github.com/libjxl/libjxl.git||v{ver}"
        self.description = "JPEG XL image format reference implementation"
        self.patchLevel["0.11.1"] = 1
        self.defaultTarget = "0.11.1"

    def setDependencies(self):
        self.runtimeDependencies["libs/brotli"] = None
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
            "-DJPEGXL_ENABLE_SKCMS=ON",
            "-DJPEGXL_ENABLE_TCMALLOC=OFF",
            "-DJPEGXL_FORCE_SYSTEM_BROTLI=ON",
            "-DJPEGXL_FORCE_SYSTEM_HWY=ON",
            "-DBUILD_TESTING=OFF",
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
