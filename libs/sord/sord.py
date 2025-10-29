# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Lightweight C library for storing RDF statements in memory"
        self.webpage = "https://drobilla.net/software/sord"

        self.svnTargets["master"] = "https://gitlab.com/drobilla/sord.git"
        self.patchLevel["master"] = 20250808

        for ver in ["0.16.16", "0.16.18"]:
            self.targets[ver] = f"https://download.drobilla.net/sord-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"sord-{ver}"
        self.targetDigests["0.16.16"] = (["257f876d756143da02ee84c9260af93559d6249dd87f317e70ab5fffcc975fd0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.16.18"] = (["4f398b635894491a4774b1498959805a08e11734c324f13d572dea695b13d3b3"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.16.18"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
