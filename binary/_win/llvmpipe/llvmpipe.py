# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2024 Thomas Friedrichsmeier <thomas.friedrichsmeier@kdemail.net>
import info
import utils
from CraftCore import CraftCore
from CraftCompiler import CraftCompiler
from Utils import CraftHash
from Package.BinaryPackageBase import BinaryPackageBase

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["11.2.2", "12.0.rc2"]:
            dashver = ver.replace('.', '_')
            bits = '64' if CraftCore.compiler.architecture == CraftCompiler.Architecture.x86_64 else '32'
            self.targets[ver] = f"https://download.qt.io/development_releases/prebuilt/llvmpipe/windows/opengl32sw-{bits}-mesa_{dashver}.7z"
        self.targetDigests["11.2.2"] = (["142a74bfbe7d2b1bf633925f130b29eb10ffa9fb87cc1bbd05ee2624ee81d261"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["12.0.rc2"] = (["2a0d2f92c60e0962ef5f6039d3793424c6f39e49ba27ac04a5b21ca4ae012e15"], CraftHash.HashAlgorithm.SHA256)
        self.webpage = "https://docs.mesa3d.org/drivers/llvmpipe.html"
        self.description = "Software rasterizer OpenGL implementation"

        self.defaultTarget = "12.0.rc2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def install(self):
        utils.copyDir(self.sourceDir(), self.installDir() / "bin")

        return True
