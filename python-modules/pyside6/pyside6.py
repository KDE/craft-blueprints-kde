# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2025 Stefan Gerlach <stefan.gerlach@uni.kn>

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Python Qt bindings project"

        for ver in ["6.9.3"]:
            self.svnTargets[ver] = f"git://code.qt.io/pyside/pyside-setup.git||v{ver}"
            self.targetInstSrc[ver] = "."

        self.defaultTarget = "6.9.3"

    def setDependencies(self):
        self.runtimeDependencies["libs/python"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args = [
                f"-DCMAKE_C_FLAGS=-isystem {CraftCore.standardDirs.craftRoot()}/include/python3.11",
                f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}"
                ]
        self.supportsNinja = False
