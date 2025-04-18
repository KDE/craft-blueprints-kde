# SPDX-FileCopyrightText: 2026 Melvin Keskin <melvo@olomono.de>
#
# SPDX-License-Identifier: CC0-1.0

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/protobuf-c/protobuf-c.git"
        for ver in ["1.5.2"]:
            self.targets[ver] = f"https://github.com/protobuf-c/protobuf-c/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"protobuf-c-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"protobuf-c-{ver}"
            self.targetConfigurePath[ver] = "build-cmake"
        self.targetDigests["1.5.2"] = (["cea46eeaa19c52924938b582c5d128a6ed3b6fb5b3f4677476a1781cc06e03f3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.5.2"

    def setDependencies(self):
        self.buildDependencies["libs/protobuf"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            # Only build libprotobuf-c, not protoc which is the other part of protobuf-c.
            "-DBUILD_PROTOC=OFF",
        ]
