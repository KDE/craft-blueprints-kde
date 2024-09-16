# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["20201020"]:
            self.targets[ver] = "https://www.prevanders.net/libdwarf-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libdwarf-" + ver

        self.patchLevel["20201020"] = 0
        self.targetDigests["20201020"] = (
            ["5c1078440c4afc255ce9597e1fca96615b9b41c88fe33c18a1fdc140ec1dee835bd926473535fcacb2f8d3c8fd63349c24e89e71a2d1a2319408a970f7bfa320"],
            CraftHash.HashAlgorithm.SHA512,
        )

        self.description = "Libdwarf is a C library intended to simplify reading (and writing) applications using DWARF2, DWARF3, DWARF4 and DWARF5."
        self.defaultTarget = "20201020"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.platform = ""
