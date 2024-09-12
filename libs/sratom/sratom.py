# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.6.16"]:
            self.targets[ver] = f"https://download.drobilla.net/sratom-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"sratom-{ver}"
        self.targetDigests["0.6.16"] = (["71c157991183e53d0555393bb4271c75c9b5f5dab74a5ef22f208bb22de322c4"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.6.16"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
