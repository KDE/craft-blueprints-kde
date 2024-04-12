# -*- coding: utf-8 -*-
import os

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.2.9"]:
            self.targets[ver] = f"https://gitea.nouspiro.space/nou/libXISF/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"libxisf-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libxisf"
        self.description = "A C++ library that can read and write XISF files produced by PixInsight."
        self.defaultTarget = "0.2.9"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzstd"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        self.subinfo.options.configure.args += ["-DCMAKE_MACOSX_RPATH=1", "-DUSE_BUNDLED_ZLIB=OFF", f"-DCMAKE_INSTALL_RPATH={craftLibDir}"]
