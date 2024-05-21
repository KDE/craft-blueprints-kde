# SPDX-FileCopyrightText: 2019 Hannah von Reth <vonreth@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/npth")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
