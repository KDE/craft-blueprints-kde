# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = (
            "LibVNCServer/LibVNCClient are cross-platform C libraries that allow you to easily implement VNC server or client functionality in your program"
        )
        self.webpage = "https://libvnc.github.io/"
        for ver in ["0.9.14"]:
            self.targets[ver] = f"https://github.com/LibVNC/libvncserver/archive/refs/tags/LibVNCServer-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libvncserver-LibVNCServer-{ver}"
        self.targetDigests["0.9.14"] = (["83104e4f7e28b02f8bf6b010d69b626fae591f887e949816305daebae527c9a5"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/LibVNC/libvncserver.git"
        self.defaultTarget = "0.9.14"

    def setDependencies(self):
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libsdl2"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DWITH_EXAMPLES=OFF",
            "-DWITH_GTK=OFF",
            f"-DWITH_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
        ]
