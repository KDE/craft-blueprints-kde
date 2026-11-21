# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.7.4"]:
            self.targets[ver] = f"https://github.com/randy408/libspng/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libspng-{ver}"
        self.targetDigests["0.7.4"] = (["47ec02be6c0a6323044600a9221b049f63e1953faf816903e7383d4dc4234487"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["0.7.4"] = [
            ("libspng-0.7.4-20261015.diff", 1),
            # https://github.com/microsoft/vcpkg/blob/20ceb8adbf0504d4b0d5e4058a32f9d4fc896391/ports/libspng/fix-spngconfig-cmake.patch#L1
            ("fix-spngconfig-cmake.patch", 1),
        ]

        self.description = (
            "libspng (simple png) is a C library for reading and writing Portable Network Graphics (PNG) format files with a focus on security and ease of use."
        )
        self.webpage = "https://libspng.org/"
        self.releaseManagerId = 24289
        self.defaultTarget = "0.7.4"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supportsCCACHE = False
        self.subinfo.options.configure.args += [
            "-DBUILD_EXAMPLES=OFF",
            f"-DSPNG_STATIC={self.subinfo.options.buildStatic.asOnOff}",
            f"-DSPNG_SHARED={self.subinfo.options.buildStatic.inverted.asOnOff}",
        ]
