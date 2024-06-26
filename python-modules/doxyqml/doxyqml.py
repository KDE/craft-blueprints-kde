# -*- coding: utf-8 -*-
import os

import info
from CraftOS.osutils import OsUtils
from Package.PipPackageBase import PipPackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.buildDependencies["dev-utils/python3"] = None

    def setTargets(self):
        self.svnTargets["master"] = ""
        self.patchLevel["master"] = 1
        self.description = "Doxyqml is an input filter for Doxygen, a documentation system for C++ and a few other languages."
        self.defaultTarget = "master"


class Package(PipPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.python2 = False

    def install(self):
        if OsUtils.isWin():
            utils.createShim(
                self.imageDir() / "bin/doxyqml.exe",
                self.imageDir() / "dev-utils/bin/python3.exe",
                args=[os.path.join(CraftCore.settings.get("Paths", "Python"), "Scripts", "doxyqml")],
            )
        return PipBuildSystem.install(self)
