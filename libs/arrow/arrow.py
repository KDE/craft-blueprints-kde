# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Apache Arrow C++ library with Parquet support"
        self.webpage = "https://arrow.apache.org/"

        for ver in ["26.0.1"]:
            url = f"https://archive.apache.org/dist/arrow/arrow-{ver}/apache-arrow-{ver}.tar.gz"
            self.targets[ver] = url
            self.targetInstSrc[ver] = f"apache-arrow-{ver}"
            # fetch the checksum from Apache instead of hardcoding it
            self.targetDigestUrls[ver] = (url + ".sha256", CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "26.0.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        self.runtimeDependencies["libs/liblz4"] = None
        self.runtimeDependencies["libs/brotli"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/thrift"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DARROW_PARQUET=ON",
            "-DARROW_BUILD_STATIC=OFF",
            "-DARROW_BUILD_SHARED=ON",
            "-DARROW_DEPENDENCY_USE_SHARED=ON",
            "-DARROW_WITH_SNAPPY=OFF",
            "-DARROW_WITH_BROTLI=ON",
            "-DARROW_WITH_LZ4=ON",
            "-DARROW_WITH_ZSTD=ON",
            "-DARROW_WITH_ZLIB=ON",
            "-DARROW_WITH_BZ2=ON"
        ]

    def configureSourceDir(self):
        return self.sourceDir() / "cpp"
