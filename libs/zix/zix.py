# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A lightweight C library of portability wrappers and data structures"
        self.webpage = "https://github.com/drobilla/zix"

        self.svnTargets["master"] = "https://github.com/drobilla/zix.git"
        self.patchLevel["master"] = 20250808

        for ver in ["0.4.2", "0.6.2"]:
            self.targets[ver] = f"https://download.drobilla.net/zix-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"zix-{ver}"
        self.targetDigests["0.4.2"] = (["0c071cc11ab030bdc668bea3b46781b6dafd47ddd03b6d0c2bc1ebe7177e488d"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.6.2"] = (["4bc771abf4fcf399ea969a1da6b375f0117784f8fd0e2db356a859f635f616a7"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.6.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
