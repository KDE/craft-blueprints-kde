# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "dot.conf configuration file parser"

        for ver in ["1.3"]:
            self.targets[ver] = f"https://github.com/williamh/dotconf/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dotconf-{ver}"
        self.targetDigests["1.3"] = (["7f1ecf40de1ad002a065a321582ed34f8c14242309c3547ad59710ae3c805653"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/williamh/dotconf.git"
        self.patchLevel["master"] = 20220321

        self.defaultTarget = "1.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
