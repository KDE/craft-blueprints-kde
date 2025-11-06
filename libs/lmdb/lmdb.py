# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils.CraftBool import CraftBool


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.16"]:
            self.targets[ver] = f"https://github.com/LMDB/lmdb/archive/LMDB_{ver}.tar.gz"
            self.targetInstSrc[ver] = "lmdb-LMDB_" + ver + "/libraries/liblmdb"
        self.patchToApply["0.9.16"] = [("lmdb-LMDB_0.9.16-20151004.diff", 3)]
        self.targetDigests["0.9.16"] = "367182e1d9dbc314db76459a71be719209f131b4"
        self.patchLevel["0.9.16"] = 1

        self.description = "in memory database from the openldap project"
        self.defaultTarget = "0.9.16"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            f"-DBUILD_TESTS={CraftBool(self.subinfo.options.dynamic.buildStatic and self.subinfo.options.dynamic.buildTests).asOnOff}",
            f"-DBUILD_TOOLS={CraftBool(self.subinfo.options.dynamic.buildStatic and self.subinfo.options.dynamic.buildTools).asOnOff}",
            f"-DBUILD_STATIC={self.subinfo.options.dynamic.buildStatic.asOnOff}",
        ]
