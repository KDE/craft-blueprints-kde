# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2024 Julius Künzel <julius.kuenzel@kde.org>

import info
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "FreeRDP is a free remote desktop protocol library and clients"
        self.webpage = "http://www.freerdp.com/"
        for ver in ["2.11.7", "3.8.0"]:
            self.targets[ver] = f"https://github.com/FreeRDP/FreeRDP/releases/download/{ver}/freerdp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"freerdp-{ver}"
        self.targetDigests["2.11.7"] = (["5a2d54e1ca0f1facd1632bcc94c73b9f071a80c5fdbbb3f26e79f02aaa586ca3"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.8.0"] = (["b068fff34e6256806deb5bcdfe9a213955850abe056d162f2b166510e4a63823"], CraftHash.HashAlgorithm.SHA256)

        if CraftCore.compiler.compiler.isMinGW:
            # https://github.com/msys2/MINGW-packages/tree/66db4d3812a8b1bfde805246d2d0c97d0d9307ec/mingw-w64-freerdp
            self.patchToApply["2.11.7"] = [(".2.11.7-mingw", 1)]

        self.svnTargets["master"] = "https://github.com/FreeRDP/FreeRDP.git"
        self.defaultTarget = "2.11.7"

    def setDependencies(self):
        self.runtimeDependencies["libs/libusb"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if CraftCore.compiler.compiler.isMinGW:
            self.subinfo.options.dynamic.buildTests = False
        if CraftCore.compiler.platform.isMacOS and CraftCore.compiler.architecture.isX86_64:
            self.subinfo.options.configure.args += ["-DWITH_NEON=OFF"]

    def fixEncoding(self, filename):
        with open(filename, "rb") as file:
            content = file.read()

        decoded_content = content.decode("utf-16le")

        with open(filename, "wb") as file:
            file.write(decoded_content.encode("utf-8"))

    def unpack(self):
        if not super().unpack():
            return False
        if CraftCore.compiler.compiler.isMinGW and self.buildTarget < CraftVersion("3.0.0"):
            self.fixEncoding(self.sourceDir() / "client/Windows/wfreerdp.rc")
        return True
