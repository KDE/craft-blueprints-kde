# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Volker Krause <vkrause@kde.org>
import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        if not CraftCore.compiler.isAndroid and not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/qt6/qtwebengine"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
