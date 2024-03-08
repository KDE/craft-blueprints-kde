# -*- coding: utf-8 -*-
import os

import info
import utils
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for branch in ["master", "release"]:
            self.svnTargets[branch] = "[git]git://cmake.org/cmake.git|%s" % branch
            self.targetInstallPath[branch] = os.path.join("dev-utils", "cmake-src")

        self.defaultTarget = "release"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args = ["-DKWSYS_INSTALL_LIB_DIR=lib", "-DKWSYS_INSTALL_INCLUDE_DIR=include"]

    def install(self):
        if not super().install():
            return False
        for name in ["cmake", "cmake-gui", "cmcldeps", "cpack", "ctest"]:
            if not utils.createShim(self.imageDir() / f"dev-utils/bin/{name}.exe", self.imageDir() / f"dev-utils/cmake/bin/{name}.exe"):
                return False
        return True
