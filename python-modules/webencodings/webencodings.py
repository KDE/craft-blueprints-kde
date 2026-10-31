# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Julius Künzel <julius.kuenzel@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.6.1"]:
            self.svnTargets[ver] = ""
        self.description = "Character encoding for the web."
        self.webpage = "https://github.com/gsnedders/python-webencodings"
        self.defaultTarget = "0.6.1"
        self.releaseManagerId = 231400

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/flit-core"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
