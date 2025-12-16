# -*- coding: utf-8 -*-
import os

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.2"]:
            self.targets[ver] = f"https://github.com/steve-m/librtlsdr/archive/refs/tags/{ver}.tar.gz"
            self.archiveNames[ver] = f"librtlsdr-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"librtlsdr-{ver}"
        self.description = "Use Realtek DVT-T dongles as a cheap SDR"
        self.defaultTarget = "2.0.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libusb"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        # both examples and tests can be run here
        self.subinfo.options.configure.args += ["-DCMAKE_MACOSX_RPATH=1", f"-DCMAKE_INSTALL_RPATH={craftLibDir}"]
