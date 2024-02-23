# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Graph Visualization Tools"
        self.webpage = "https://graphviz.org"
        for ver in ["10.0.1"]:
            self.targets[ver] = f"https://gitlab.com/graphviz/graphviz/-/archive/{ver}/graphviz-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"graphviz-{ver}"

        self.targetDigests["10.0.1"] = (["28f452ef1cb12288c8758a62f8c3fcfefdb91b251f7aae61d0d703f851bde931"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://gitlab.com/graphviz/graphviz.git"

        self.defaultTarget = "10.0.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
