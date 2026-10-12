# SPDX-FileCopyrightText: 2026 Tobias Fella <tobias.fella@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/kdab/cxx-qt-cmake.git||main"

        for ver in ["0.10.0"]:
            self.targets[ver] = "https://github.com/kdab/cxx-qt-cmake/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "cxx-qt-cmake-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "cxx-qt-cmake-%s" % ver

        self.targetDigests["0.10.0"] = (["bbf0095649d820d26ebcd91fbfbef3dbc2894de4dd10066c46927388abceacd3"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.10.0"
        self.description = "The CMake code associated with CXX-Qt."

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
