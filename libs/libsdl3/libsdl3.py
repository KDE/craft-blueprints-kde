# SPDX-FileCopyrightText: 2026 Ian Monroe <imonroe@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        ver = "3.4.16"
        self.targets[ver] = f"https://github.com/libsdl-org/SDL/releases/download/release-{ver}/SDL3-{ver}.tar.gz"
        self.targetInstSrc[ver] = f"SDL3-{ver}"
        self.targetDigests[ver] = (
            ["7322236cd12090c3eb40b9728be4d49c76f66ad17d04369584d4ecad5cf77c68"],
            CraftHash.HashAlgorithm.SHA256,
        )
        self.description = "Simple DirectMedia Layer"
        self.webpage = "https://www.libsdl.org/"
        self.defaultTarget = ver
        self.releaseManagerId = 4777

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = [
            f"-DSDL_SHARED={self.subinfo.options.dynamic.buildStatic.inverted.asOnOff}",
            f"-DSDL_STATIC={self.subinfo.options.dynamic.buildStatic.asOnOff}",
            f"-DSDL_TEST_LIBRARY={self.subinfo.options.dynamic.buildTests.asOnOff}",
            f"-DSDL_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DSDL_EXAMPLES=OFF",
            "-DSDL_DISABLE_INSTALL_DOCS=ON",
            "-DSDL_X11_XSCRNSAVER=OFF",
        ]
