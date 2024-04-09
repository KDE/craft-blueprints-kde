# SPDX-FileCopyrightText: 2023 George Florea Bănuș <georgefb899@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.GCCLike

    def setTargets(self):
        self.displayName = "libplacebo"
        self.description = "Reusable library for GPU-accelerated image/video processing primitives and shaders, as well a batteries-included, extensible, high-quality rendering pipeline (similar to mpv's vo_gpu). Supports Vulkan, OpenGL, Metal (via MoltenVK) and Direct3D 11."
        self.svnTargets["2805a0d0"] = "https://code.videolan.org/videolan/libplacebo||2805a0d01c029084ab36bf5d0e3c8742012a0b27"
        self.svnTargets["master"] = "https://code.videolan.org/videolan/libplacebo"
        self.defaultTarget = "2805a0d0"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += ["-Ddemos=False"]
