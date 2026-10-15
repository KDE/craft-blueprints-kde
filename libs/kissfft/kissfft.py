# SPDX-FileCopyrightText: 2026 Ian Monroe <imonroe@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "131.2.0"
        self.targets[ver] = f"https://github.com/mborgerding/kissfft/archive/refs/tags/{ver}.tar.gz"
        self.targetInstSrc[ver] = f"kissfft-{ver}"
        self.targetDigests[ver] = (
            ["205a8f6a448ef12b091f8ac6a514b5091bb5f6b0b543431ed75f673116cf5cbf"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "A fast Fourier transform library"
        self.webpage = "https://github.com/mborgerding/kissfft"
        self.defaultTarget = ver
        self.releaseManagerId = 328415

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = [
            "-DKISSFFT_DATATYPE=float",
            f"-DKISSFFT_TEST={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DKISSFFT_TOOLS=OFF",
            f"-DKISSFFT_STATIC={self.subinfo.options.dynamic.buildStatic.asOnOff}",
            "-DCMAKE_INSTALL_LIBDIR=lib",
            "-DCMAKE_INSTALL_INCLUDEDIR=include",
            "-DKISSFFT_PKGCONFIG=OFF",  # just use the cmake files
        ]
