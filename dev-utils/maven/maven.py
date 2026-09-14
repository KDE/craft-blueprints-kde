# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.runtimeDependencies["dev-utils/jdk"] = None

    def setTargets(self):
        self.targets["3.9.16"] = "https://dlcdn.apache.org/maven/maven-3/3.9.16/binaries/apache-maven-3.9.16-bin.tar.gz"
        self.targetDigests["3.9.16"] = (["80ffca22aed9e8b9713a232f3394fd81d7f20322df75efdb2b047dbd3e3a23bb"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.9.16"
        self.targetInstallPath["3.9.16"] = "dev-utils/maven"
        self.targetInstSrc["3.9.16"] = "apache-maven-3.9.16"
        self.description = "Apache Maven is a software project management and comprehension tool."


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        if not super().install():
            return False
        env = {"JAVA_HOME": CraftPackageObject.get("dev-utils/jdk").instance.JAVA_HOME}
        return utils.createShim(
            self.imageDir() / "dev-utils/bin/mvn", self.installDir() / f"bin/mvn{'.cmd' if CraftCore.compiler.isWindows else ''}", env=env
        ) and utils.createShim(self.imageDir() / "dev-utils/bin/mvn", self.installDir() / f"bin/mvn{'.cmd' if CraftCore.compiler.isWindows else ''}", env=env)
