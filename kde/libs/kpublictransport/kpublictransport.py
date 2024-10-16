# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2019 Nicolas Fella <nicolas.fella@gmx.de>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/kpublictransport.git")
        self.description = "Library for accessing public transport data"

        # Fix Android with Qt 6.8
        # See https://invent.kde.org/libraries/kpublictransport/-/merge_requests/85
        self.patchToApply["24.08.2"] = [("85.patch", 1)]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
