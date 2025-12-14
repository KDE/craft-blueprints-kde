# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash
from Utils.CraftBool import CraftBool


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.33"]:
            self.targets[ver] = f"https://git.openldap.org/openldap/openldap/-/archive/LMDB_{ver}/openldap-LMDB_{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openldap-LMDB_{ver}/libraries/liblmdb"
        self.patchToApply["0.9.33"] = [("lmdb-LMDB_0.9.16-20151004.diff", 3), ("lmdb-0.9.33-20251126.diff", 3)]
        self.targetDigests["0.9.33"] = (["476801f5239c88c7de61c3390502a5d13965ecedef80105b5fb0fcb8373d1e53"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["0.9.33"] = 1
        self.defaultTarget = "0.9.33"

        self.description = "in memory database from the openldap project"
        self.releaseManagerId = 6974
        self.webpage = "https://symas.com/lmdb/"

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
