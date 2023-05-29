# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Laurent Montel <montel@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Text Addons (autocorrection, grammar checking, text to speak, translator support)"
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/ktextaddons")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["libs/qt5/qtspeech"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
