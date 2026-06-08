# SPDX-FileCopyrightText: 2026 Tobias Fella <tobias.fella@kde.org>
# SPDX-License-Identifier: LGPL-2.0-or-later

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Performance-portable, length-agnostic SIMD with runtime dispatch "
        self.svnTargets["master"] = "https://github.com/google/highway"

        for ver in ["1.4.0"]:
            self.targets[ver] = f"https://github.com/google/highway/releases/download/{ver}/highway-{ver}.tar.gz"
            self.archiveNames[ver] = f"highway-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"highway-{ver}"

        self.targetDigests["1.4.0"] = (["36f672ab48ddb3c8555e9e89e16fe400cd7d16c6eb455a1a3d0c146a63ababdc"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.4.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
