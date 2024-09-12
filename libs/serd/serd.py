# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.32.2"]:
            self.targets[ver] = f"https://download.drobilla.net/serd-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"serd-{ver}"
        self.targetDigests["0.32.2"] = (["df7dc2c96f2ba1decfd756e458e061ded7d8158d255554e7693483ac0963c56b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.32.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
