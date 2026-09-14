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
        self.targets["7.25.0"] = "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.25.0/openapi-generator-cli-7.25.0.jar"
        self.targetDigests["7.25.0"] = (["41ce4f6b07f196676439d710759fa1ced7a08066d06ff1bf314681470289efae"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "7.25.0"
        self.targetInstallPath["7.25.0"] = "dev-utils/bin"
        self.description = "OpenAPI Generator CLI is a command-line tool for generating code from OpenAPI specifications."


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def make(self):
        if not utils.moveFile(self.workDir() / self.subinfo.archiveName()[0], self.workDir() / "openapi-generator-cli.jar"):
            return False
        return super().make()

    def postInstall(self):
        return utils.createShim(
            self.installDir() / "openapi-generator-cli",
            CraftPackageObject.get("dev-utils/jdk").instance.JAVA_HOME / f"bin/java{CraftCore.compiler.executableSuffix}",
            ["-jar", self.installDir() / "openapi-generator-cli.jar"],
            useAbsolutePath=True,
            env={"JAVA_HOME": CraftPackageObject.get("dev-utils/jdk").instance.JAVA_HOME},
        )
