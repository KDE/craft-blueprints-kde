# SPDX-FileCopyrightText: 2026 by Hannah von Reth <vonreth@kde.org>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "QHauk"  # not final
        self.description = "Hauk is a fully open source, self-hosted location sharing service. "

        self.svnTargets["master"] = "https://invent.kde.org/vonreth/qhauk.git"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtopenapi"] = None
        self.runtimeDependencies["libs/qt6/qtlocation"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
