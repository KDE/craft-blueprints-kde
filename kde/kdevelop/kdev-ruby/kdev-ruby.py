# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>
# SPDX-FileCopyrightText: 2017 Hannah von Reth <vonreth@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/kdevelop/kdev-ruby"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.description = "ruby support for kdevelop"
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.runtimeDependencies["kde/kdevelop/kdevelop"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
