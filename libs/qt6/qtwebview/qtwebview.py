# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Volker Krause <vkrause@kde.org>
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        if not CraftCore.compiler.platform.isAndroid and not CraftCore.compiler.platform.isMacOS:
            self.runtimeDependencies["libs/qt6/qtwebengine"] = None


from Package.CMakePackageBase import *


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
