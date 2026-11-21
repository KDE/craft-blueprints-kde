# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.34.2"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "2.34.2"
        self.releaseManagerId = 4004

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/setuptools"] = None
        self.runtimeDependencies["python-modules/charset-normalizer"] = None
        self.runtimeDependencies["python-modules/idna"] = None
        self.runtimeDependencies["python-modules/urllib3"] = None
        self.runtimeDependencies["python-modules/certifi"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
