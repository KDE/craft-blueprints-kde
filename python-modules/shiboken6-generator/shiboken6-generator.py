# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings generator to create Python wrapper"
        self.defaultTarget = "6.9.2"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allowPrebuildBinaries = True
        self.subinfo.options.configure.args += ["-v", "-v", "-v"]
