# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Hannah von Reth <vonreth@kde.org>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.86.0"]:
            self.targets[ver] = f"https://github.com/boostorg/boost/releases/download/boost-{ver}/boost-{ver}-cmake.tar.xz"
            self.targetDigestUrls[ver] = (
                f"https://github.com/boostorg/boost/releases/download/boost-{ver}/boost-{ver}-cmake.tar.xz.txt",
                CraftHash.HashAlgorithm.SHA256,
            )
            self.targetInstSrc[ver] = f"boost-{ver}"
        self.defaultTarget = "1.86.0"
        self.webpage = "https://www.boost.org/"

        self.description = "Boost provides free peer-reviewed portable C++ source libraries."

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/icu"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/python"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # https://github.com/boostorg/cmake
        self.subinfo.options.configure.args += [
            "-DBOOST_INCLUDE_LIBRARIES=atomic;chrono;date-time;filesystem;iostreams;program_options;python;random;regex;safe_numerics;serialization;signals2;system;thread",
        ]
        if not CraftCore.compiler.platform.isAndroid:
            self.subinfo.options.configure.args += ["-DBOOST_ENABLE_PYTHON=ON"]

        if CraftCore.compiler.platform.isWindows:
            cxx_flags = ["-D_WIN32_WINNT=0x0A00", "-DWINVER=0x0A00", "-D_WIN32_IE=0x0A00"]
            if CraftCore.compiler.compiler.isMSVC:
                cxx_flags += ["-EHsc"]

            cxx_flags_str = " ".join(cxx_flags)
            self.subinfo.options.configure.args += [f"-DCMAKE_CXX_FLAGS={cxx_flags_str}"]
