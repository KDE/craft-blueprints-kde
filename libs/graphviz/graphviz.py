# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Graph Visualization Tools"
        self.webpage = "https://graphviz.org"
        for ver in ["10.0.1"]:
            # We need to use git since the tarballs do not contain the submudules needed on Windows
            self.svnTargets[ver] = f"https://gitlab.com/graphviz/graphviz.git||{ver}"

        self.svnTargets["master"] = "https://gitlab.com/graphviz/graphviz.git"

        self.defaultTarget = "10.0.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.fetch.checkoutSubmodules = True
