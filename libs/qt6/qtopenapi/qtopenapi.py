# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import os

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["6.11.1"] = [("qtopenapi-6.11.1-20260914.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.buildDependencies["dev-utils/jdk"] = None
        self.buildDependencies["dev-utils/openapi-generator-cli"] = None
        self.buildDependencies["dev-utils/maven"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        javaHome = CraftPackageObject.get("dev-utils/jdk").instance.JAVA_HOME
        with utils.ScopedEnv({"JAVA_HOME": javaHome, "PATH": f"{javaHome}/bin{os.path.pathsep}{os.environ['PATH']}"}):
            return super().configure()
