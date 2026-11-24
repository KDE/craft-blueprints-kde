# SPDX-FileCopyrightText: 2025 Tobias Fella <tobias.fella@kde.org>
# SPDX-License-Identifier: LGPL-2.0-or-later

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Marrying Rust and CMake - Easy Rust and C/C++ Integration!"
        self.svnTargets["master"] = "https://github.com/corrosion-rs/corrosion"

        for ver in ["0.6.1"]:
            self.targets[ver] = f"https://github.com/corrosion-rs/corrosion/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"corrosion-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"corrosion-{ver}"

        self.targetDigests["0.6.1"] = (["e9e95b1ee2bad52681f347993fb1a5af5cce458c5ce8a2636c9e476e4babf8e3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.6.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
