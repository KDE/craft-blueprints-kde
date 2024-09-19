# SPDX-License-Identifier: LGPL-3.0
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.18.2"]:
            self.targets[ver] = f"https://github.com/strukturag/libheif/releases/download/v{ver}/libheif-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libheif-{ver}"
        self.targetDigests["1.18.2"] = (["c4002a622bec9f519f29d84bfdc6024e33fd67953a5fb4dc2c2f11f67d5e45bf"], CraftHash.HashAlgorithm.SHA256)
        self.description = "libheif is an HEIF and AVIF file format decoder and encoder"
        self.defaultTarget = "1.18.2"

    def setDependencies(self):
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/openjpeg"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DENABLE_PLUGIN_LOADING=OFF",
            "-DWITH_LIBSHARPYUV=OFF",
            "-DWITH_EXAMPLES=OFF",
            "-DWITH_GDK_PIXBUF=OFF",
            "-DBUILD_TESTING=OFF",
            "-DWITH_LIBDE265=OFF",
            "-DWITH_X265=OFF",
            "-DWITH_AOM_DECODER=OFF",
            "-DWITH_AOM_ENCODER=OFF",
            "-DWITH_JPEG_DECODER=ON",
            "-DWITH_OpenJPEG_DECODER=ON",
            "-DWITH_FFMPEG_DECODER=ON",
        ]
