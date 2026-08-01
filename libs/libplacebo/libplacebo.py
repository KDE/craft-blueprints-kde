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
        self.svnTargets["7.360.1"] = "https://code.videolan.org/videolan/libplacebo||v7.360.1"
        self.svnTargets["master"] = "https://code.videolan.org/videolan/libplacebo"
        self.defaultTarget = "7.360.1"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.fetch.checkoutSubmodules = True
        self.subinfo.options.configure.args += ["-Ddemos=False"]

        if CraftCore.compiler.isAndroid:
            # Work around https://github.com/android/ndk/issues/1974 in ndk26.
            # But also Vulkan video decode isn't well supported on Android anyway.
            self.subinfo.options.configure.args += ["-Dvulkan=disabled"]
