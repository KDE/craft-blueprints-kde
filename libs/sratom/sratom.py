# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Library for serialising LV2 atoms"
        self.webpage = "https://drobilla.net/software/sratom"

        self.svnTargets["master"] = "https://gitlab.com/lv2/sratom.git"
        self.patchLevel["master"] = 20250808

        for ver in ["0.6.16", "0.6.18"]:
            self.targets[ver] = f"https://download.drobilla.net/sratom-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"sratom-{ver}"
        self.targetDigests["0.6.16"] = (["71c157991183e53d0555393bb4271c75c9b5f5dab74a5ef22f208bb22de322c4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.6.18"] = (["4c6a6d9e0b4d6c01cc06a8849910feceb92e666cb38779c614dd2404a9931e92"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.6.18"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-Ddocs=disabled"]
