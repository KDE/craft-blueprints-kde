# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Volker Krause <vkrause@kde.org>
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        if not CraftCore.compiler.isAndroid and not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/qt5/qtwebengine"] = None


from Package.Qt5CorePackageBase import *


class Package(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
