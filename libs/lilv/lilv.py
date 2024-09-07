# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.24.24"]:
            self.targets[ver] = f"https://download.drobilla.net/lilv-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"lilv-{ver}"
        self.targetDigests["0.24.24"] = (["6bb6be9f88504176d0642f12de809b2b9e2dc55621a68adb8c7edb99aefabb4f"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.24.24"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["libs/zix"] = None
        self.buildDependencies["libs/serd"] = None
        self.buildDependencies["libs/sord"] = None
        self.buildDependencies["libs/lv2"] = None
        self.buildDependencies["libs/sratom"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
