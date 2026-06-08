# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Prayag Jain <prayagjain2@gmail.com>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "md4qt"
        self.description = "md4qt is a static C++ library for parsing Markdown"

        self.svnTargets["3810c15"] = "https://invent.kde.org/libraries/md4qt.git||3810c153cecf258bcf8c1c0d0f87c50e5654d4b3"
        self.svnTargets["master"] = "https://invent.kde.org/libraries/md4qt.git"

        self.defaultTarget = "3810c15"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
