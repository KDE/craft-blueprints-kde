# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Hannah von Reth <vonreth@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.5.0"]:
            self.targets[ver] = f"https://github.com/xiph/flac/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"flac-{ver}"
            self.archiveNames[ver] = f"flac-{ver}.tar.gz"

        self.targetDigests["1.5.0"] = (
            ["c8e119462205cfd8bbe22b0aff112625d3e51ca11de97e4de06a46fb43a0768d7ec9c245b299b09b7aa4d811c6fc7b57856eaa1c217e82cca9b3ad1c0e545cbe"],
            CraftHash.HashAlgorithm.SHA512,
        )

        self.releaseManagerId = 817
        self.description = "Free Lossless Audio Codec"
        self.webpage = "https://xiph.org/flac/"
        self.defaultTarget = "1.5.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DBUILD_PROGRAMS=ON",
            "-DBUILD_EXAMPLES=OFF",
            "-DBUILD_TESTING=OFF",
            "-DBUILD_DOCS=OFF",
            "-DINSTALL_MANPAGES=OFF",
            "-DWITH_OGG=ON",
        ]
