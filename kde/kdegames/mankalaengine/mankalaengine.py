# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Rana Ali Hassnain <ranaalihassnain07@gmail.com>

import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/games/mankalaengine.git"
        self.defaultTarget = "master"
        self.description = "Mankala Engine"

        self.options.dynamic.registerOption("buildExamples", False)
        self.options.dynamic.registerOption("buildDocumentation", False)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            f"-DBUILD_EXAMPLES={self.subinfo.options.dynamic.buildExamples.asOnOff}",
            f"-DBUILD_DOC={self.subinfo.options.dynamic.buildDocumentation.asOnOff}"
        ]
