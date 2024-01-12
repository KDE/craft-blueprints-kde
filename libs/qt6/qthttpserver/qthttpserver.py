# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 g10 Code GmbH
# SPDX-Contributor: Carl Schwan <carl.schwan@gnupg.com>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
