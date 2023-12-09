# SPDX-FileCopyrightText: 2023 George Florea Bănuș <georgefb899@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import info
from Package.MesonPackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "libplacebo"
        self.description = "Reusable library for GPU-accelerated image/video processing primitives and shaders, as well a batteries-included, extensible, high-quality rendering pipeline (similar to mpv's vo_gpu). Supports Vulkan, OpenGL, Metal (via MoltenVK) and Direct3D 11."
        self.svnTargets["master"] = "https://code.videolan.org/videolan/libplacebo"
        self.defaultTarget = "6.338.1"

        for ver in ["6.338.1"]:
            self.targets[ver] = f"https://code.videolan.org/videolan/libplacebo/-/archive/v{ver}/libplacebo-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libplacebo-v{ver}"
            self.archiveNames[ver] = f"libplacebo-v{ver}.tar.gz"

    def setDependencies(self):
        self.buildDependencies["python-modules/meson"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["python-modules/glad2"] = None
        self.runtimeDependencies["python-modules/jinja2"] = None

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-Ddemos=False"]
