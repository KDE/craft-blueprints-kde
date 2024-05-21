# SPDX-FileCopyrightText: 2019 Hannah von Reth <vonreth@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/gnupg")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/npth"] = None
        self.runtimeDependencies["libs/libksba"] = None
        # sqlite is only needed for keyboxd; we ignore it for now
        # self.runtimeDependencies["libs/sqlite"] = None
        self.runtimeDependencies["libs/ntbtls"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
