# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/pim/itinerary.git")
        self.description = "Digital travel assistant app"

        for ver in ["23.04.3"]:
            self.patchToApply[ver] = [("0001-android-qt5-15-10-gradle-oom-fix.patch", 1), ("0002-android-qt5-15-10-ndk-fix.patch", 1)]
            self.patchLevel[ver] = 1
        self.patchToApply["23.08.0"] = [("0001-Manually-manage-permissions-in-the-Android-manifest.patch", 1)]
        self.patchLevel["23.08.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5" and CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/prison"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kunitconversion"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/libs/kosmindoormap"] = None
        self.runtimeDependencies["kde/libs/kpublictransport"] = None
        self.runtimeDependencies["kde/pim/kitinerary"] = None
        self.runtimeDependencies["kde/pim/kpkpass"] = None
        self.runtimeDependencies["kde/plasma-mobile/khealthcertificate"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if self.buildTarget == "master":
            self.runtimeDependencies["qt-libs/libquotient"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
