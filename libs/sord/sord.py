# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.16.16"]:
            self.targets[ver] = f"https://download.drobilla.net/sord-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"sord-{ver}"
        self.targetDigests["0.16.16"] = (["257f876d756143da02ee84c9260af93559d6249dd87f317e70ab5fffcc975fd0"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.16.16"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
