# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C/C++ library for retrieving information on files and directories "
        self.webpage = "https://github.com/tronkko/dirent"
        for ver in ["1.26"]:
            self.targets[ver] = f"https://github.com/tronkko/dirent/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dirent-{ver}"

        self.targetDigests["1.26"] = (["a91662ee5243d2dae5aee7ed8527f95097afda517cc5cc7ca2699648a74a419c"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/tronkko/dirent.git"

        self.defaultTarget = "1.26"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
