# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        # On other platforms we use gettext instead
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Android

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/j-jorge/libintl-lite.git"
        self.defaultTarget = "master"
        self.description = "libintl lite - gettext replacement for Android"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
