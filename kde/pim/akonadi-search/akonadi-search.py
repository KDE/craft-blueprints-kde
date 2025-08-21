# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Julius Künzel <julius.kuenzel@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Libraries and daemons to implement searching in Akonadi"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/krunner"] = None

        self.runtimeDependencies["kde/pim/akonadi"] = None
        self.runtimeDependencies["kde/pim/akonadi-mime"] = None
        self.runtimeDependencies["kde/pim/kmime"] = None

        self.runtimeDependencies["kde/libs/ktextaddons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
