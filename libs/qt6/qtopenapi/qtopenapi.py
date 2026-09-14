# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["dev-utils/jdk"] = None
        self.runtimeDependencies["dev-utils/openapi-generator-cli"] = None
        self.runtimeDependencies["dev-utils/maven"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        with utils.ScopedEnv({"JAVA_HOME": CraftPackageObject.get("dev-utils/jdk").instance.JAVA_HOME}):
            return super().configure()
