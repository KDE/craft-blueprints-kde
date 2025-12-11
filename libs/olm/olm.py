# SPDX-FileCopyrightText: 2022 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildStatic", True)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://gitlab.matrix.org/matrix-org/olm"
        for ver in ["3.2.14", "3.2.16"]:
            self.targets[ver] = f"https://gitlab.matrix.org/matrix-org/olm/-/archive/{ver}/olm-{ver}.tar.gz"
            self.archiveNames[ver] = f"olm-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"olm-{ver}"
        self.targetDigests["3.2.14"] = (["221e2e33230e8644da89d2064851124b04e9caf846cad2aaa3626b876b42d14a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.2.16"] = (["1e90f9891009965fd064be747616da46b232086fe270b77605ec9bda34272a68"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.2.16"] = [("const.diff", 0)]

        self.defaultTarget = "3.2.16"

        self.releaseManagerId = 29706
        self.description = "C++ library for Olm encryption"
        self.webpage = "https://gitlab.matrix.org/matrix-org/olm"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DOLM_TESTS=OFF"]
