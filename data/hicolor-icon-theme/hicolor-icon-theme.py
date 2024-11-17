# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>
# SPDX-FileCopyrightText: 2017 Hannah von Reth <vonreth@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.18"]:
            self.targets[ver] = f"https://icon-theme.freedesktop.org/releases/hicolor-icon-theme-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"hicolor-icon-theme-{ver}"
        self.targetDigests["0.18"] = (["db0e50a80aa3bf64bb45cbca5cf9f75efd9348cf2ac690b907435238c3cf81d7"], CraftHash.HashAlgorithm.SHA256)
        self.description = "High-color icon theme shell from the FreeDesktop project"
        self.defaultTarget = "0.18"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
