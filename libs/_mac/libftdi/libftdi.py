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
        self.subinfo.options.configure.args += ["-DPYTHON_BINDINGS=OFF", "-DEXAMPLES=OFF", "-DFTDI_EEPROM=OFF"]
        if not self.subinfo.options.dynamic.buildTests:
            self.subinfo.options.configure.args += ["-DBUILD_TESTS=OFF"]
