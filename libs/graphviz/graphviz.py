# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Graph Visualization Tools"
        self.webpage = "https://graphviz.org"
        for ver in ["10.0.1"]:
            # We need to use git since the tarballs do not contain the submudules needed on Windows
            self.svnTargets[ver] = f"https://gitlab.com/graphviz/graphviz.git||{ver}"

           self.patchToApply["10.0.1"] = [("fix-windows-install.diff", 1)]
        self.patchLevel["10.0.1"] = 1

        self.svnTargets["master"] = "https://gitlab.com/graphviz/graphviz.git"

        self.defaultTarget = "10.0.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/bison"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args = ["-Dwith_gvedit=OFF"]