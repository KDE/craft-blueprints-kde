# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2021 Volker Krause <vkrause@kde.org>

import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        # On other platforms we use gettext instead
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Android

    def setTargets(self):

        self.description = "libintl lite - gettext replacement for Android"

        self.svnTargets["ba15146"] = "https://github.com/j-jorge/libintl-lite.git||ba1514607d02ce3711d828e784a7e9e2bb25aa84"
        self.svnTargets["master"] = "https://github.com/j-jorge/libintl-lite.git"

        self.defaultTarget = "ba15146"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
