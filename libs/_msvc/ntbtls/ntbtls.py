# SPDX-FileCopyrightText: 2023 g10 Code GmbH
# SPDX-FileContributor: Carl Schwan <carl.schwan@gnupg.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.BinaryPackageBase import BinaryPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/ntbtls")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/libksba"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
