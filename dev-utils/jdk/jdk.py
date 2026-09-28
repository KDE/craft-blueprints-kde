# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2026 Hannah von Reth <vonreth@kde.org>
from pathlib import Path
from urllib import parse

import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

    def setTargets(self):
        if CraftCore.compiler.architecture == CraftCore.compiler.Architecture.x86_64:
            arch = "x64"
        elif CraftCore.compiler.architecture == CraftCore.compiler.Architecture.arm64:
            arch = "aarch64"
        else:
            raise NotImplementedError()

        for ver in ["25.0.4.1+1"]:
            urlVer = parse.quote(ver)
            tarVer = ver.replace("+", "_")
            self.targetInstSrc[ver] = f"jdk-{ver}"
            if CraftCore.compiler.isWindows:
                self.targets[
                    ver
                ] = f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_windows_hotspot_{tarVer}.zip"
                self.targetDigestUrls[ver] = (
                    [
                        f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_windows_hotspot_{tarVer}.zip.sha256.txt"
                    ],
                    CraftHash.HashAlgorithm.SHA256,
                )
            elif CraftCore.compiler.isMacOS:
                self.targets[
                    ver
                ] = f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_mac_hotspot_{tarVer}.tar.gz"
                self.targetDigestUrls[ver] = (
                    [
                        f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_mac_hotspot_{tarVer}.tar.gz.sha256.txt"
                    ],
                    CraftHash.HashAlgorithm.SHA256,
                )
            elif CraftCore.compiler.isLinux:
                self.targets[
                    ver
                ] = f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_linux_hotspot_{tarVer}.tar.gz"
                self.targetDigestUrls[ver] = (
                    [
                        f"https://github.com/adoptium/temurin25-binaries/releases/download/jdk-{urlVer}/OpenJDK25U-jdk_{arch}_linux_hotspot_{tarVer}.tar.gz.sha256.txt"
                    ],
                    CraftHash.HashAlgorithm.SHA256,
                )
            else:
                raise NotImplementedError()
            self.targetInstallPath[ver] = "dev-utils/jdk"
            self.defaultTarget = "25.0.4.1+1"
        self.description = "Java Runtime Environment"


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def JAVA_HOME(self) -> Path:
        if CraftCore.compiler.isMacOS:
            return self.installPrefix() / "Contents/Home"
        return self.installPrefix()
