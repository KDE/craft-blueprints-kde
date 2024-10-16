# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "KDE OSM Indoor Map"
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/kosmindoormap.git")

        # Fix Android with Qt 6.8
        # See https://invent.kde.org/libraries/kosmindoormap/-/merge_requests/45
        self.patchToApply["24.08.2"] = [("45.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/recastnavigation"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/libs/kopeninghours"] = None
        self.runtimeDependencies["kde/libs/kpublictransport"] = None
        # needed for the app
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcontacts"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/openssl"] = None
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None

    def registerOptions(self):
        self.options.dynamic.registerOption("buildStandaloneApp", False)


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_STANDALONE_APP=" + ("ON" if self.subinfo.options.dynamic.buildStandaloneApp else "OFF")]
