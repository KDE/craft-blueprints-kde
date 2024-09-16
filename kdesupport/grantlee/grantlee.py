# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/steveire/grantlee.git"
        self.targets["5.3.1"] = "https://github.com/steveire/grantlee/archive/v5.3.1.tar.gz"
        self.targetDigests["5.3.1"] = (["ba288ae9ed37ec0c3622ceb40ae1f7e1e6b2ea89216ad8587f0863d64be24f06"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["5.3.1"] = "grantlee-5.3.1"
        self.defaultTarget = "5.3.1"

        self.patchToApply["5.3.1"] = []
        if CraftCore.compiler.platform.isMacOS:
            self.patchToApply["5.3.1"] += [("0001-Don-t-use-dot-in-folder-name-to-prevent-macOS-issues.patch", 1)]
        self.patchToApply["5.3.1"] += [("grantlee-5.3.1-20201117.diff", 1)]
        self.patchLevel["5.3.1"] = 2

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
