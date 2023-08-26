# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "DB Browser for SQLite"

        self.defaultTarget = "3.12.0"
        self.targets[self.defaultTarget] = f"https://github.com/sqlitebrowser/sqlitebrowser/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"sqlitebrowser-{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"sqlitebrowser-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (["3f1a1453ed0f4b5b72b0468bf8ee56887eb23d71c2518a449f4eb179471d73d1"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/sqlite"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        if CraftCore.compiler.isMacOS:
            # make sure to use our sqlite header and not the apple one...
            self.subinfo.options.configure.args = f'-DCMAKE_CXX_FLAGS="-isystem {CraftCore.standardDirs.craftRoot()}/include"'
