# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.1.0"]:
            self.svnTargets[ver] = ""
        self.defaultTarget = "3.1.0"
        self.releaseManagerId = 138380
        self.description = "Seamless operability between C++11 and Python"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/pip"] = None
        self.runtimeDependencies["libs/python"] = None
        self.buildDependencies["python-modules/scikit-build-core"] = None
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["dev-utils/ninja"] = None


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--config-settings=strict-config=false"]
