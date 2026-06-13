# SPDX-License-Identifier: LGPL-3.0
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.23.0"]:
            self.targets[ver] = f"https://github.com/strukturag/libheif/releases/download/v{ver}/libheif-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libheif-{ver}"
        self.targetDigests["1.23.0"] = (["4c9182b18897617182eed12ab5eb9f9d855b3aa3a736d6bdb31abc034ec7d393"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.23.0"] = [("libheif-1.18.2-20250415.diff", 1)]
        self.description = "libheif is an HEIF and AVIF file format decoder and encoder"
        self.defaultTarget = "1.23.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/openjpeg"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DBUILD_DOCUMENTATION=OFF",
            "-DENABLE_PLUGIN_LOADING=OFF",
            "-DWITH_LIBSHARPYUV=OFF",
            "-DWITH_EXAMPLES=OFF",
            "-DWITH_GDK_PIXBUF=OFF",
            "-DWITH_LIBDE265=OFF",
            "-DWITH_X265=OFF",
            "-DWITH_AOM_DECODER=OFF",
            "-DWITH_AOM_ENCODER=OFF",
            "-DWITH_JPEG_DECODER=ON",
            "-DWITH_OpenJPEG_DECODER=ON",
            "-DWITH_FFMPEG_DECODER=ON",
            "-DWITH_OpenH264_DECODER=OFF",
            "-DWITH_X264=OFF",
        ]
