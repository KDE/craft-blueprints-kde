# SPDX-FileCopyrightText: 2022 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://gitlab.matrix.org/matrix-org/olm"
        for ver in ["3.2.14"]:
            self.targets[ver] = f"https://gitlab.matrix.org/matrix-org/olm/-/archive/{ver}/olm-{ver}.tar.gz"
            self.archiveNames[ver] = f"olm-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"olm-{ver}"
        self.targetDigests["3.2.14"] = (["221e2e33230e8644da89d2064851124b04e9caf846cad2aaa3626b876b42d14a"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.2.14"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DBUILD_SHARED_LIBS=OFF -DOLM_TESTS=OFF"
