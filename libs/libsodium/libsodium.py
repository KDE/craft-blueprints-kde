# SPDX-FileCopyrightText: 2021 Tobias Fella <fella@posteo.de>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.AutoToolsPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/jedisct1/libsodium"
        for ver in ["1.0.18"]:
            self.targets[ver] = "https://github.com/jedisct1/libsodium/archive/refs/tags/%s-RELEASE.zip" % ver
            self.archiveNames[ver] = "libsodium-%s-RELEASE.zip" % ver
            self.targetInstSrc[ver] = "libsodium-%s-RELEASE" % ver
        self.targetDigests["1.0.18"] = (["7728976ead51b0de60bede2421cd2a455c2bff3f1bc0320a1d61e240e693bce9"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "1.0.18"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.autoreconf = False
