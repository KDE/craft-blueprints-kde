# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2019 Nicolas Fella <nicolas.fella@gmx.de>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/kpublictransport.git")
        self.description = "Library for accessing public transport data"

        self.patchToApply["26.04.1"] = [("6ace248b71ea3fe6211a67b3fa0d3452ba59dd4a.diff", 1)]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtlocation"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
