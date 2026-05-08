# SPDX-License-Identifier: LGPL-3.0
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.21.2"]:
            self.targets[ver] = f"https://github.com/strukturag/libheif/releases/download/v{ver}/libheif-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libheif-{ver}"
        self.targetDigests["1.21.2"] = (["75f530b7154bc93e7ecf846edfc0416bf5f490612de8c45983c36385aa742b42"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.21.2"] = [("libheif-1.18.2-20250415.diff", 1)]
        self.description = "libheif is an HEIF and AVIF file format decoder and encoder"
        self.defaultTarget = "1.21.2"

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
