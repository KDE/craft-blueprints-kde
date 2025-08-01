# SPDX-License-Identifier: LGPL-3.0
# SPDX-FileCopyrightText: 2024 Daniel Novomesky <dnovomesky@gmail.com>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.19.8"]:
            self.targets[ver] = f"https://github.com/strukturag/libheif/releases/download/v{ver}/libheif-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libheif-{ver}"
        self.targetDigests["1.19.8"] = (["6c4a5b08e6eae66d199977468859dea3b5e059081db8928f7c7c16e53836c906"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.19.8"] = [("libheif-1.18.2-20250415.diff", 1)]
        self.description = "libheif is an HEIF and AVIF file format decoder and encoder"
        self.defaultTarget = "1.19.8"

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
