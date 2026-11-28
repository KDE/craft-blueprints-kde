# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Apache Thrift C++ library"
        self.webpage = "https://thrift.apache.org/"

        for ver in ["0.25.0"]:
            url = f"https://archive.apache.org/dist/thrift/{ver}/thrift-{ver}.tar.gz"
            self.targets[ver] = url
            self.targetInstSrc[ver] = f"thrift-{ver}"
            # fetch the checksum from Apache instead of hardcoding it
            self.targetDigestUrls[ver] = (url + ".sha256", CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.25.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DBUILD_TESTING=OFF",
            "-DBUILD_COMPILER=OFF",
            "-DBUILD_CPP=ON",
            "-DBUILD_LIBRARIES=ON",
            "-DBUILD_TUTORIALS=OFF",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_PYTHON=OFF",
            "-DBUILD_JAVA=OFF",
            "-DBUILD_JAVASCRIPT=OFF",
            "-DBUILD_NODEJS=OFF",
            "-DWITH_LIBEVENT=OFF",
            "-DWITH_OPENSSL=OFF",
            "-DWITH_QT5=OFF",
            "-DWITH_ZLIB=ON",
            "-DWITH_SHARED_LIB=ON",
            "-DWITH_STATIC_LIB=OFF",
        ]
