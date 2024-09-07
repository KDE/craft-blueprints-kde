# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.18.10"]:
            self.targets[ver] = f"https://lv2plug.in/spec/lv2-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"lv2-{ver}"
        self.targetDigests["1.18.10"] = (["78c51bcf21b54e58bb6329accbb4dae03b2ed79b520f9a01e734bd9de530953f"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.18.10"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
