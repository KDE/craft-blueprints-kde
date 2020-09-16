# -*- coding: utf-8 -*-

import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.8.0", "3.10.1", "3.12.0"]:
            self.targets[ver] = f"https://github.com/sqlitebrowser/sqlitebrowser/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"sqlitebrowser-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"sqlitebrowser-{ver}"
        self.patchToApply["3.10.1"] = [("sqlitebrowser-3.10.1.diff", 1)]
        self.targetDigests["3.8.0"] = (["f638a751bccde4bf0305a75685e2a72d26fc3e3a69d7e15fd84573f88c1a4d92"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.10.1"] = (['36eb53bc75192c687dce298c79f1532c410ce4ecbeeacfb07b9d02a307f16bef'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.12.0"] = (['3f1a1453ed0f4b5b72b0468bf8ee56887eb23d71c2518a449f4eb179471d73d1'], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "3.12.0"
        self.description = "DB Browser for SQLite"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/sqlite"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DUSE_QT5=ON"
