# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "A library implementing the EBU R128 loudness standard."
        self.webpage = "https://github.com/jiixyj/libebur128"
        for ver in ["1.2.6"]:
            self.targets[ver] = f"https://github.com/jiixyj/libebur128/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libebur128-{ver}"

        self.targetDigests["1.2.6"] = (["baa7fc293a3d4651e244d8022ad03ab797ca3c2ad8442c43199afe8059faa613"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/jiixyj/libebur128t.git"

        self.defaultTarget = "1.2.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", f"-DENABLE_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff()}"]
