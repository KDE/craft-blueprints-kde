# -*- coding: utf-8 -*-
import os

import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4"]:
            self.targets[ver] = f"https://www.intra2net.com/en/developer/libftdi/download/libftdi1-{ver}.tar.bz2"
            self.archiveNames[ver] = f"libftdi1-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libftdi1-{ver}"
        self.description = "Library to talk to FTDI chips"
        self.defaultTarget = "1.4"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["libs/swig"] = None
        self.buildDependencies["libs/libusb"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DPYTHON_BINDINGS=OFF", "-DEXAMPLES=OFF", "-DBUILD_TESTS=OFF"]

    def postQmerge(self):
        packageName = "libftdi1"
        root = str(CraftCore.standardDirs.craftRoot())
        craftLibDir = os.path.join(root, "lib")
        utils.system("install_name_tool -add_rpath " + craftLibDir + " " + craftLibDir + "/" + packageName + ".dylib")
        utils.system("install_name_tool -id @rpath/" + packageName + ".dylib " + craftLibDir + "/" + packageName + ".dylib")
        return True
